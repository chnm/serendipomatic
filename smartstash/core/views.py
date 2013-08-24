from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
from social_auth.models import UserSocialAuth
import logging
from pyzotero import zotero
import time
import guess_language
import random

# from smartstash.core import zotero
from smartstash.core.forms import InputForm, ZoteroInputForm
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
    # since this is the site index

    if request.method == 'GET':
        # on get request, initialize an empty form for display
        form = InputForm()

        if request.user.is_authenticated():
            zotero_form = ZoteroInputForm(user=request.user)
        else:
            zotero_form = None

    elif request.method == 'POST':
        # on post, init form based on posted data
        # if form is invalid, redisplay input form with error messages

        submit_type = request.POST.get('submit')

        if submit_type == 'text_input':
            form = InputForm(request.POST)
        elif submit_type == 'zotero_input':
            form = ZoteroInputForm(data=request.POST, user=request.user)

        if form.is_valid():

            # TODO: break out into sub function (?)
            if submit_type == 'text_input':

                # actual logic here - infer search terms, query apis, display stuff

                text = form.cleaned_data['text']
                search_terms = {}

                lang = guess_language.guessLanguage(text)
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

            # TODO: probably should also be separate function
            elif submit_type == 'zotero_input':
                selection = form.cleaned_data['selection']

                # retrieve zotero user info to get zotero access
                zotero_user = UserSocialAuth.objects.get(user=request.user, provider='zotero')
                zot = zotero.Zotero(zotero_user.uid, 'user', zotero_user.tokens['oauth_token'])
                if selection == 'recent':
                    items = zot.items(limit=100)
                else:
                    seltype, val = selection.split(':')
                    if seltype == 'collection':
                        items = zot.collection_items(val)
                    elif seltype == 'group':
                        zotgrp = zotero.Zotero(val, 'group', zotero_user.tokens['oauth_token'])
                        items = zotgrp.items(limit=100)
                    elif seltype == 'tag':
                       items = zot.tag_items(val)

                textdata = []
                # TODO: logic for generating text/search terms from zotero items should be
                # in a separate method or class
                for item in items:
                    if item['itemType'] == 'note':
                        textdata.append(item['note'])  # might be html ?
                    else:
                        data = []
                        for field in ['title', 'abstractNote']:
                            if field in item:
                                data.append(item[field])
                        for creator in item.get('creators', []):
                            data.append('%(firstName)s %(lastName)s' % creator)
                        textdata.append(' '.join(data))


                text = ' '.join(textdata)
                search_terms = common_words(text)

                # sanitize
                for key, val in search_terms.iteritems():
                    # val is a list of terms
                    search_terms[key] = [escape(v) for v in val]

        # if form is valid,
        # for either text input or zotero where we got terms

        # store search terms in the session so we can redirect
        request.session['search_terms'] = search_terms

        # redirect
        # NOTE: should probably be http code 303, see other
        return HttpResponseRedirect(reverse('discoveries:view'))

        # if not valid: pass through and redisplay errors

    return render(request, 'core/site_index.html',
                  {'input_form': form, 'zotero_form': zotero_form})



# TODO: view copied from display.views, code probably needs to be refactored
# into a single app
def sanitizeString(s):
    result = ""
    for c in s: result += escapes.get(c, c)
    return result


def view_items(request):
    search_terms = request.session.get('search_terms', None)

    error_messages = {
        'no_terms': '''Whoops! Somehow we didn't come up with any search
            terms for you. Put some different text in the box and we'll
            give it another go.''',
        'no_results': '''Our sources couldn't find anything for the
            search terms created from your text. Put some different text
            in the box and we'll give it another go.'''
    }


    # if no search terms, return to site index
    if search_terms is None or not search_terms['keywords']:

        if search_terms is not None and 'keywords' in search_terms:
            messages.error(request, error_messages['no_terms'])

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
    request.session['items'] = items

    # if none of the API calls worked, message & return to home page
    if not items:
        # if error is true, at least one of the api calls failed
        # otherwise, presumably we callled all apis and didn't get any results (?)
        messages.error(request, error_messages['no_terms'])
        return HttpResponseRedirect(reverse('site-index'))

    # shuffle images so we get a more even mix, esp. if one source
    # (such as flickr) returns more items than the others
    random.shuffle(items)

    # NOTE: we may need to clear the cache when we do a 'start over'....

    return render(request, 'core/view.html',
                  {'items': items, 'query_terms': search_terms, 'sources': sources})


def save_list(request):
    items = request.session.get('items', None)
    # no items to save; error & redirect to index
    if items is None:
        messages.error(request, '''Whoops! Somehow we didn't find any discoveries to save.''')
        return HttpResponseRedirect(reverse('site-index'))

    search_terms = request.session['search_terms']  # TODO: error handling if not set
    # (should be set if items are set)
    sources = [DPLA, Europeana, Flickr, Trove] # TODO: shared list
    return render(request, 'core/save_list.html',
                  {'items': items, 'query_terms': search_terms, 'sources': sources})

