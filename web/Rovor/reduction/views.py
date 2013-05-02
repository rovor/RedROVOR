from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

@login_required
def index(request):
    '''Index page for reduction'''
    return render(request,'reduction/index.html')
    
    
