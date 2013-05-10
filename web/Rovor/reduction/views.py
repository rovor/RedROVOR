from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from action_views import renameAll, makeZero

import logging
logger = logging.getLogger('Rovor')   

# Create your views here.

@login_required
def index(request):
    '''Index page for reduction'''
    return render(request,'reduction/index.html')

@login_required
def zeroDark(request):
    '''Page for doing zeros and darks'''
    return render(request,'reduction/zeroDark.html')

@login_required
def flatApply(request):
    '''Page for applying flats'''
    return HttpResponse("<h1>Under Construction</h1>")

@login_required
def astrometry(request):
    '''Page for doing astrometry'''
    return HttpResponse("<h1>Under Construction</h1>")




    
