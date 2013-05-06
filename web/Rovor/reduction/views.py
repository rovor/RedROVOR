from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from redrovor import renamer
from dirmanage.models import Filesystem
import json

#import logging

#logger = logging.getLogger('Rovor')
import logging
logger = logging.getLogger('django')   # Django's catch-all logger
hdlr = logging.StreamHandler()   # Logs to stderr by default
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

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

@login_required
def renameAll(request):
    '''rename all files in a folder to be .fit instead of .FIT'''
    #return HttpResponse(json.dumps(request.POST),mimetype='application/json')
    if request.method != 'POST' or not 'path' in request.POST:
        logger.info('Invalid request')
        raise Http404 #should only be accessed by POST method, with a path argument
    try:
        path = Filesystem.getTruePath(request.POST['path'])
        logger.info('Renaming files in: ' + path)
    except (ValueError, Filesystem.DoesNotExist, IOError):
        logger.info('Attempted access to invalid path: ' + request.POST['path'])
        return HttpResponse('{"ok":false,"error":"Invalid path"}',mimetype='application/json')
    renamer.renameAll(path) #rename the files
    return HttpResponse('{"ok":true}',mimetype='application/json')


    
