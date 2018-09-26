from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    """ main page view """ 
    
    return HttpResponse('<html><title>TODO Lists</title></html>')
