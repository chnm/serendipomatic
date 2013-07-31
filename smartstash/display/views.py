# Create your views here.

from django.shortcuts import render

from smartstash.find.models import DPLA

def view_results(request):
	items = DPLA.find_items(['dog', 'cat'])
	return render(request, 'display/view.html',
		{'items': items})
