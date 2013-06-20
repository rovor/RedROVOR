from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView

from redrovor.secondpass import  SecondPassProcessor
from photcontrol import getObjectMapping


#import some views from another module, this allows some seperation
#between views used for html and views used for AJAX
from action_views import renameAll, makeZero, makeDark, makeFlats, \
    subZeroDark, firstPass, applyFlats, applyWCS, secondPass


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

class DirSelect(TemplateView):
    start_path = '/'
    handler = None #function (view) which takes the request and the true path to a directory and returns a response

    template_name= 'reduction/dirSelect.html'

    def get_context_data(self, **kwargs):
        '''get context to use for rendering template'''
        context = super(DirSelect, self).get_context_data(**kwargs)
        context['start_path'] = self.start_path
        return context

    def post(self, request, *args, **kwargs):
        '''respond to post when a form was submitted'''
        if 'path' not in request.POST:
            return HttpResponseBadRequest()
        try:
            path = Filesystem.getTruePath(request.POST['path'])
        except:
            context = self.get_context_data(error='Invalid path, try again')
            return self.render_to_response(context)
        return self.handler(request,path)

    @classmethod
    def decorate(cls, start_path='/'):
        '''decorate a function to make it the response
        to selecting the folder'''
        def decorator(f):
            return cls.as_view(start_path=start_path, handler=f)
        return decorator


@login_required
@DirSelect.decorate('Processed/')
def flatSelectForm(request, path):
    '''Form for selecting flats'''
    context = {'improc':SecondPassProcessor(path), 'path':path}
    return render(request, 'reduction/flatFrameSelect.html',context)


@login_required
@DirSelect.decorate('Processed/')
def photometry_start(request,path):
    '''Page for doing astrometry'''
    mapping, missing = getObjectMapping(path)
    if missing:
        return HttpResponse("Missing coordinates for: "+', '.join(missing))
    else:
        return HttpResponse("All coordinates accounted for")
    

