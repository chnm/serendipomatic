from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import logging
import time
import guess_language
import random

from smartstash.core import zotero
from smartstash.core.forms import InputForm
from smartstash.core.utils import common_words, get_search_terms
from smartstash.core.api import DPLA, Europeana, Flickr

from smartstash.auth.models import ZoteroUser
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

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


def site_index(request):
    # preliminary site index page

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

    #clear the session
    for key, value in request.session.items():
        if key != 'search_terms': del request.session[key]

    # if no search terms, return to site index
    if search_terms is None:
        return HttpResponseRedirect(reverse('site-index'))

    # sanitize the search terms for API queries
    search_terms['keywords'] = [sanitizeString(s) for s in search_terms['keywords']]

    start = time.time()
    dpla_items = DPLA.find_items(**search_terms)
    euro_items = Europeana.find_items(**search_terms)
    # added Flickr
    flkr_items = Flickr.find_items(**search_terms)
    logger.info('Queried 3 sources in %.2f sec' % (time.time() - start))

    sources = [DPLA, Europeana, Flickr]

    # combine all results into a single list and then shuffle them together
    logger.info('Number of items by source: DPLA=%d, Europeana=%d, Flickr=%d' % \
                 (len(dpla_items), len(euro_items), len(flkr_items)))
    items = dpla_items + euro_items + flkr_items
    # shuffle images so we get a more even mix, esp. if one source
    # (such as flickr) returns more items than the others
    random.shuffle(items)

    # NOTE: we may need to clear the cache when we do a 'start over'....

    return render(request, 'core/view.html',
                  {'items': items, 'query_terms': search_terms, 'sources': sources})

def dummy1(request):
    output = 'Lorem ipsum &c.'
    return render(request, 'dummy1.html',
                  {'output': output})

def dummy2(request):
    output = 'Lorem ipsum &c. &c.'
    return render(request, 'dummy2.html',
                  {'output': output})

def dummy3(request):
    output = 'Lorem ipsum &c. &c. &c.'
    return render(request, 'dummy3.html',
                  {'output': output})

def saveme(request):

    search_terms = request.session['search_terms']  # TODO: error handling if not set
    dpla_items = DPLA.find_items(**search_terms)
    euro_items = Europeana.find_items(**search_terms)
    flkr_items = Flickr.find_items(**search_terms)
    sources = [DPLA, Europeana]
    items = [x for t in zip(dpla_items, euro_items, flkr_items) for x in t]
    return render(request, 'core/saveme.html',
                  {'items': items, 'query_terms': search_terms, 'sources': sources})
