
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.views.generic import View

import logging

logger = logging.getLogger('Rovor')

from dirmanage.models import Filesystem

import json

import traceback



class PathProcessView(View):
    '''View class for Views that want to use the true path from
    a path provided by the 'path' POST request
    '''

    http_method_names = ['post','options']  #only allow post requests
    error_mimetype='text/plain'
    invalidPathResult = 'Invalid path'
    noPathResult = "no path supplied"
    innerView = None #lambda request,path: return HttpResponse("")  #default behaviour is to do nothing

    def post(self,request):
        '''method to wrap the code for getting the true path
        and calling the actual code, which takes too paramaters,
        the request object and the path and returns an HttpResponse'''
        if 'path' in request.POST:
            try: 
                path = Filesystem.getTruePath(request.POST['path'])
            except (ValueError, Filesystem.DoesNotExist, IOError):
                logger.info("Attempted access to invalid path: "+request.POST['path'])
                return HttpResponseBadRequest(self.invalidPathResult, mimetype=error_mimetype)
            return self.innerView(request,path)
        else:
            return HttpResponseBadRequest(noPathResult, mimetype=error_mimetype)

    @classmethod
    def decorate(cls, innerView):
        '''decorate a function innerView and change it into a view as 
        returned by as_view
        the function should take two paramaters: 
        @param request the request object
        @param path the true path on the server machine'''
        return cls.as_view(innerView=innerView)
    @classmethod
    def pathOnly(cls, innerFunc):
        '''decorate a function which takes only one paramater, the true path
        and return a view which will call that function with the true path
        '''
        return cls.as_view(innerView= lambda req,path: innerFunc(path))




def process_path(request, block):
    '''
    @deprecated[use the PathProcessView and PathProcessView.decorate instead]
    
    helper function to abstract common code when accessing 
    a path over POST method. This will check that the method is POST
    and that path is a supplied field and a valid path, if it is not
    it will return a proper HttpResponse. If path is a valid path,
    then this will call block, passing in the true filesystem path to
    block, and will return the result wrapped in a HttpResponse 
    after dumping the object as a json string
    
    if block returns None the result
    will simply be {"ok":true} '''
    try:
        res = PathProcessView.pathOnly(block)(request)
    except Exception as err:
        #if there was some kind of uncaught exception return it to the client
        resp = {"ok":False, "error":str(err), "errtype":type(err).__name__,"traceback":traceback.format_exc()}
        return HttpResponse(json.dumps(resp),mimetype='application/json')
    #default to simply responding an ok response if return was false
    if res is None:
        res = '{"ok":true}'
    else:
        res = json.dumps(res)
    return HttpResponse(res,mimetype='application/json')
