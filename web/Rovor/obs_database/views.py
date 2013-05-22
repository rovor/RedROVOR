# Create your views here.

from django.http import HttpResponse, Http404

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie


from redrovor import obsRecord
from dirmanage.toolset import PathProcessView

import logging

logger = logging.getLogger('Rovor')


@login_required
@ensure_csrf_cookie
def upload_form(request):
    '''form fo uploading observation from a folder on the server''' 
    return render(request,'obs_database/upload_form.html')


@login_required
@PathProcessView.pathOnly
def processFolder(path):
    obsRecord.recordDir
    return HttpResponse('{"ok":true}',mimetype='application/json')

