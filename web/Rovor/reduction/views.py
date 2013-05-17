from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from redrovor import reduction


#import some views from another module, this allows some seperation
#between views used for html and views used for AJAX
from action_views import renameAll, makeZero, makeDark, \
    makeFlats, subZeroDark, firstPass


from dirmanage.models import Filesystem

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
def flatSelectForm(request):
    '''Form for selecting flats'''
    if 'path' in request.POST:
        try:
            path = Filesystem.getTruePath(request.POST['path'])
        except (ValueError, Filesystem.DoesNotExist, IOError):
            return render(request,'reduction/flatDirSelect.html',{'error':'Invalid path, try again'})
            
        context = {'improc':reduction.ImProcessor(path)}
        return render(request, 'reduction/flatFrameSelect.html',context)
    else:
        #we haven't gotten a path yet, so display page to select path
        return render(request,'reduction/flatDirSelect.html')

@login_required
def astrometry(request):
    '''Page for doing astrometry'''
    return HttpResponse("<h1>Under Construction</h1>")




    
