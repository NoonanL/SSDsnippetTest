from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def snippetTestView(request):
	return render(request, 'home.html')