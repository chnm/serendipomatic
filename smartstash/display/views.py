# Create your views here.

from django.shortcuts import render

from smartstash.find.models import DPLA

def view_results(request):
    query_terms = ['dog', 'cat']
    items = DPLA.find_items(query_terms)
    return render(request, 'display/view.html',
        {'items': items, 'query_terms': ', '.join(query_terms)})