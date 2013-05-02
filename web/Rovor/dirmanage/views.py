# Create your views here.

from django.http import HttpResponse, Http404
from django.template import Context, loader
from django.contrib.auth.decorators import login_required

from dirmanage.models import Filesystem

import json

@login_required
def index(request):
    fslist = Filesystem.objects.order_by('name')
    template = loader.get_template('dirmanage/index.html')
    c = Context({'fslist': fslist})
    return HttpResponse(template.render(c))


@login_required
def directory(request,filesystem_name,path):
    try:
        fs = Filesystem.objects.get(name=filesystem_name)
        if fs.isdir(path):
            files = fs.files(path)
            template = loader.get_template('dirmanage/directory.html')
            context = Context( { 
                'dlist': [ f for (f, d, t) in files if d],
                'flist': [ {'name':f, 'type':t} for (f,d,t) in files if not d],
                'path': path,
                'fs': fs,
            })
            return HttpResponse(template.render(context))
        else:
            (f, mimetype) = fs.file(path)
            return HttpResponse(open(f).read(),mimetype=mimetype)

    except ValueError: 
        raise Http404
    except Filesystem.DoesNotExist:
        raise Http404
    except IOError:
        raise Http404

@login_required
def chooseFrame(request,filesystem_name, path):
    try:
        fs = Filesystem.objects.get(name=filesystem_name)
        if fs.isdir(path):
            files = fs.files(path)
            template = loader.get_template('dirmanage/FileChooser.html')
            context = Context( {
                'dlist': [ f for (f,d,t) in files if d],
                'flist': [ f for (f,d,t) in files if not d and t == 'image/fits'],
                'path': path,
                'fs': fs,
            })
            return HttpResponse(template.render(context))
        else:
            raise Http404
    
    except ValueError: 
        raise Http404
    except Filesystem.DoesNotExist:
        raise Http404
    except IOError:
        raise Http404

@login_required
def testChoose(request):
    template = loader.get_template('dirmanage/chooseTest.html')
    context = Context({})
    return HttpResponse(template.render(context))

@login_required
def  getJson(request, filesystem_name, path):
    '''get a json object containing a list with the contents of the 
    path along with information about whether or not it is a directory and the mime type'''
    try:
        fs = Filesystem.objects.get(name=filesystem_name)
        if fs.isdir(path):
            files = [{'file':f,'isDir':d,'type':t} for (f,d,t) in fs.files(path) ]
            return HttpResponse(json.dumps(files),mimetype='application/json')
        else:
            raise Http404 # for now no support for individual files
    except ValueError:
        raise Http404
    except Filesystem.DoesNotExist:
        raise Http404
    except IOError:
        raise Http404
