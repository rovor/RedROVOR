
from django.http import Http404, HttpResponse

import logging

logger = logging.getLogger('ROVOR')


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
