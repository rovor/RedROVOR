from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


#import some views from another module, this allows some seperation
#between views used for html and views used for AJAX
from action_views import renameAll, makeZero, makeDark, \
    makeFlats, subZeroDark, firstPass

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
def flatDirSelect(request):
    '''Page for applying flats'''
    return render(request, 'reduction/flatDirSelect.html')

@login_required
def astrometry(request):
    '''Page for doing astrometry'''
    return HttpResponse("<h1>Under Construction</h1>")




    
