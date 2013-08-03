from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
import logging
import time
import guess_language
import random

from smartstash.core import zotero
from smartstash.core.forms import InputForm
from smartstash.core.utils import common_words, get_search_terms
from smartstash.core.api import DPLA, Europeana, Flickr, Trove

logger = logging.getLogger(__name__)

# see fixme in auth.views
escapes = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    ",": "",
    ":": "",
    "-": ""
}


@require_http_methods(["GET", "POST"])   # TODO: support HEAD requests?
def site_index(request):
    # preliminary site index page

    # TODO, possibly -- might be worth supporting HEAD requests
    # since this is the site in

    if request.method == 'GET':
        # on get request, initialize an empty form for display
        form = InputForm()

    elif request.method == 'POST':
        # on post, init form based on posted data
        # if form is invalid, redisplay input form with error messages

        form = InputForm(request.POST)
        if form.is_valid():

            # actual logic here - infer search terms, query apis, display stuff

            text = form.cleaned_data['text']
            zotero_user = form.cleaned_data['zotero_user']

            search_terms = {}
            if zotero_user:
                request.session['username'] = zotero_user
                return HttpResponseRedirect(zotero.oauth_authorize_url(request))

            elif text:
                lang = guess_language.guessLanguage(text[:100])
                logger.debug('language detected as %s' % lang)
                common_terms = common_words(text, 15, lang)
                dbpedia_terms = get_search_terms(text, lang)

                # too many terms? phrase? didn't get results when combining
                # TODO: combine dbpedia + common terms; randomize from dbpedia results
                #search_terms['keywords'].extend(dbpedia_terms['keywords'])

                search_terms['keywords'] = list(dbpedia_terms['keywords'])[:10]

                # if no terms found in dbpedia, use common terms instead
                # (todo: should be some kind of combination)
                if not search_terms['keywords']:
                    search_terms['keywords'] = common_terms['keywords']

                # within dbpedia_terms there are now lists for
                # people
                # places
                # dates {'early': ,'late': }
                # people and places were reconciled against DBpedia. Dates contains
                # only four digit values and could be passed to


            # if for is valid,
            # for either text input or zotero where we got terms

            # print search_terms['keywords']
            # store search terms in the session so we can redirect
            request.session['search_terms'] = search_terms

            # insert logic for processing zotero username here
            # zotero_user = form.cleaned_data['zotero_user']

            # redirect
            # NOTE: should probably be http code 303, see other
            return HttpResponseRedirect(reverse('view-stash'))

        # if not valid: pass through and redisplay errors

    return render(request, 'core/site_index.html',
                  {'input_form': form})


# TODO: view copied from display.views, code probably needs to be refactored
# into a single app
def sanitizeString(s):
    result = ""
    for c in s: result += escapes.get(c, c)
    return result


def view_items(request):
    search_terms = request.session.get('search_terms', None)

    # if no search terms, return to site index
    if search_terms is None or not search_terms['keywords']:
        if search_terms is not None and 'keywords' in search_terms:
            messages.error(request, '''Whoops! Somehow we didn't come up with any search terms for you''')

        # TODO: add a django session message here,
        # especially if they posted data and we didn't get any keywords
        return HttpResponseRedirect(reverse('site-index'))

    # clear the session
    # TODO: should probably be more specific what we need to clear (zotero auth info?)
    # since other items may be added to the session at some point (e.g. messages)
    for key, value in request.session.items():
        if key != 'search_terms':
            del request.session[key]

    # sanitize the search terms for API queries

    # encode the search terms for safety
    search_terms['keywords'] = [sanitizeString(s) for s in search_terms['keywords']]

    start = time.time()
    error = False
    try:
        dpla_items = DPLA.find_items(**search_terms)
    except Exception as err:
        logger.error('Error querying DPLA - %s' % err)
        error = True
        dpla_items = []

    try:
        euro_items = Europeana.find_items(**search_terms)
    except Exception as err:
        logger.error('Error querying Europeana - %s' % err)
        error = True
        euro_items = []

    try:
        flkr_items = Flickr.find_items(**search_terms)
    except Exception as err:
        logger.error('Error querying Flickr - %s' % err)
        error = True
        flkr_items = []

    try:
        trove_items = Trove.find_items(**search_terms)
    except Exception as err:
        logger.error('Error querying Trove - %s' % err)
        error = True
        trove_items = []

    logger.info('Queried 4 sources in %.2f sec' % (time.time() - start))

    # TODO: should we remove from source list if we failed?
    sources = [DPLA, Europeana, Flickr, Trove]

    # combine all results into a single list and then shuffle them together
    logger.info('Number of items by source: DPLA=%d, Europeana=%d, Flickr=%d, Trove=%d' % \
                 (len(dpla_items), len(euro_items), len(flkr_items), len(trove_items)))
    items = dpla_items + euro_items + flkr_items + trove_items

    # if none of the API calls worked, message & return to home page
    if not items:
        msg = '''We couldn't find anything for you. Please try again.'''
        # if error is true, at least one of the api calls failed
        # otherwise, presumably we callled all apis and didn't get any results (?)
        messages.error(request, msg)
        return HttpResponseRedirect(reverse('site-index'))

    # shuffle images so we get a more even mix, esp. if one source
    # (such as flickr) returns more items than the others
    random.shuffle(items)

    # NOTE: we may need to clear the cache when we do a 'start over'....

    return render(request, 'core/view.html',
                  {'items': items, 'query_terms': search_terms, 'sources': sources})


def saveme(request):
    # TODO: save results needs to be built into result page so
    # we can guarantee items match, are listed in the same order, etc

    search_terms = request.session['search_terms']  # TODO: error handling if not set
    dpla_items = DPLA.find_items(**search_terms)
    euro_items = Europeana.find_items(**search_terms)
    flkr_items = Flickr.find_items(**search_terms)
    trove_items = Trove.find_items(**search_terms)
    sources = [DPLA, Europeana, Trove]
    items = [x for t in zip(dpla_items, euro_items, flkr_items, trove_items) for x in t]
    return render(request, 'core/saveme.html',
                  {'items': items, 'query_terms': search_terms, 'sources': sources})
