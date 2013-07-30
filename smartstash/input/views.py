# Create your views here.
from django.shortcuts import render


def site_index(request):
    # placeholder site index page
    return render(request, 'input/site_index.html')

