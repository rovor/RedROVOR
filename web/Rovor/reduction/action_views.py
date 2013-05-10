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


def process_path(request, block,mimetype='application/json'):
    '''helper function to abstract common code when accessing 
    a path over POST method. This will check that the method is POST
    and that path is a supplied field and a valid path, if it is not
    it will return a proper HttpResponse. If path is a valid path,
    then this will call block, passing in the true filesystem path to
    block, and will return the result wrapped in a HttpResponse with the
    given mimetype (defaults to json)'''
    if request.method != 'POST':
        logger.info('Non-POST attempt to acces POST-only resource')
        raise Http404
    if 'path' in request.POST:
        try:
            path = Filesystem.getTruePath(request.POST['path'])
        except (ValueError, Filesystem.DoesNotExist, IOError):
            logger.info('Attempted access to invalid path: '+request.POST['path'])
            return HttpResponse('{"ok":false,"error":"Invalid path"}',mimetype='application/json')
        return HttpResponse(block(path),mimetype=mimetype)
    else:
        return HttpResponse('{"ok":false,"error":"No Path supplied"}',mimetype='application/json')

@login_required
def renameAll(request):
    '''rename all files in a folder to be .fit instead of .FIT'''
    def rename_func(path):
        renamer.renameAll(path) #rename the files
        return '{"ok":true}'
    return process_path(request,rename_func)


@login_required
def makeZero(request):
    '''make a master zero from a folder'''
    def zmaker(path):
        improc = ImProcessor(path)
        logger.info("Making zero at path " + path)
        try:
            improc.makeZero()
        except ValueError as err:
            return '{{"ok":false, "error": "{0}"}}'.format(err)
        return '{"ok":true}'
    return process_path(request,zmaker)

@login_required
def makeDark(request):
    '''make a master dark from a folder'''
    def dmaker(path):
        improc = ImProcessor(path)
        logger.info("Making dark at path " + path)
        try:
            improc.makeDark()
        except ValueError as err:
            return '{{"ok:false, "error": "{0}"}}'.format(err)
        return '{"ok":true}'
    return process_path(request,dmaker)

