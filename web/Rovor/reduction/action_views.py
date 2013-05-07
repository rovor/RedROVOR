'''This is just a helper module to factor out the actions of reduction from the actual pages, everything in here is imported into the main views module'''


from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import json
import os

from redrovor import renamer
from redrovor.process import makeZero
from redrovor.reduction import ImProcessor
from dirmanage.models import Filesystem

import logging
logger = logging.getLogger('Rovor')



@login_required
def renameAll(request):
    '''rename all files in a folder to be .fit instead of .FIT'''
    #return HttpResponse(json.dumps(request.POST),mimetype='application/json')
    if request.method != 'POST' or not 'path' in request.POST:
        logger.info('Invalid request on renameAll')
        raise Http404 #should only be accessed by POST method, with a path argument
    try:
        path = Filesystem.getTruePath(request.POST['path'])
        logger.info('Renaming files in: ' + path)
    except (ValueError, Filesystem.DoesNotExist, IOError):
        logger.info('Attempted access to invalid path: ' + request.POST['path'])
        return HttpResponse('{"ok":false,"error":"Invalid path"}',mimetype='application/json')
    renamer.renameAll(path) #rename the files
    return HttpResponse('{"ok":true}',mimetype='application/json')


#@login_required
def makeZero(request):
    '''make a master zero from a folder'''
    if request.method != 'POST':
        logger.info('Non-POST attempt to access makeZero')
        raise Http404
    if 'path' in request.POST:
        try:
            path = Filesystem.getTruePath(request.POST['path'])
        except (ValueError, Filesystem.DoesNotExist, IOError):
            logger.info('Attempted access to invalid path: '+request.POST['path'])
            return HttpResponse('{"ok":false,"error":"Invalid path"}',mimetype='application/json')
        improc = ImProcessor(path)
        logger.info("Making zero at path " + path)
        try:
            improc.makeZero()
        except ValueError as err:
            return HttpResponse('{{"ok":false, "error": "{0}"}}'.format(err),mimetype='application/json')
        return HttpResponse('{"ok":true}',mimetype='application/json')
    else:
        return HttpResponse('{"ok":false,"error":"No Path supplied"}',mimetype='application/json')



        

