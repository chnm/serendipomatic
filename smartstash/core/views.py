from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from smartstash.core.forms import InputForm
from smartstash.core.utils import common_words
from smartstash.core.api import DPLA, Europeana


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
            search_terms = common_words(text, 15)
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

def view_items(request):

    search_terms = request.session['search_terms']  # TODO: error handling if not set
    dpla_items = DPLA.find_items(**search_terms)
    euro_items = Europeana.find_items(**search_terms)
    sourceDict = {'DPLA': 'http://dp.la/', 'Europeana': 'http://www.europeana.eu/'}
    sources = []
    for k, v in sourceDict.iteritems():
        item = '<a href="'+v+'" target="_blank">'+k+'</a>'
        sources.append(item)
    # quick way to shuffle the two lists together based on
    # http://stackoverflow.com/questions/11125212/interleaving-lists-in-python
    items = [x for t in zip(dpla_items, euro_items) for x in t]

    # NOTE: we may need to clear the cache when we do a 'start over'....

    return render(request, 'core/view.html',
                  {'items': items, 'query_terms': search_terms, 'sources': sources})
