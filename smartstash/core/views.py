# Create your views here.
from django.shortcuts import render

from smartstash.core.forms import InputForm
from smartstash.core.utils import common_words
from smartstash.core.api import DPLA


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
            # FIXME: redirect to new page? how to pass search terms?
            # post? or store in session?
            return view_items(request, search_terms)

        # if not valid: pass through and redisplay errors

    return render(request, 'core/site_index.html',
                  {'input_form': form})


# TODO: view copied from display.views, code probably needs to be refactored
# into a single app

def view_items(request, search_terms):
    items = DPLA.find_items(**search_terms)
    return render(request, 'core/view.html',
                  {'items': items, 'query_terms': search_terms})
