
from django.http import Http404, HttpResponse

import logging

logger = logging.getLogger('Rovor')

from dirmanage.models import Filesystem

import json


def process_path(request, block):
    '''helper function to abstract common code when accessing 
    a path over POST method. This will check that the method is POST
    and that path is a supplied field and a valid path, if it is not
    it will return a proper HttpResponse. If path is a valid path,
    then this will call block, passing in the true filesystem path to
    block, and will return the result wrapped in a HttpResponse 
    after dumping the object as a json string
    
    if block returns None the result
    will simply be {"ok":true} '''
    if request.method != 'POST':
        logger.info('Non-POST attempt to acces POST-only resource')
        raise Http404
    if 'path' in request.POST:
        try:
            path = Filesystem.getTruePath(request.POST['path'])
        except (ValueError, Filesystem.DoesNotExist, IOError):
            logger.info('Attempted access to invalid path: '+request.POST['path'])
            return HttpResponse('{"ok":false,"error":"Invalid path"}',mimetype='application/json')
        try:
            res = block(path)
        except Exception as err:
            #if there was some kind of uncaught exception return it to the client
            return HttpResponse('{{"ok":false,"error":"{0}"}}'.format(err),mimetype='application/json')
        #default to simply responding an ok response if return was false
        if res is None:
            res = '{"ok":true}'
        else:
            res = json.dumps(res)
        return HttpResponse(res,mimetype='application/json')
    else:
        return HttpResponse('{"ok":false,"error":"No Path supplied"}',mimetype='application/json')
