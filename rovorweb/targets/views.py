# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from models import Target,TargetForm, CoordFileModelForm

def index(request):
    '''index page, just view a list
    of targets in the database'''
    return HttpResponseRedirect('/targets/targetList/')




def addObject(request):
    '''add an object to the database'''
    if request.method == 'POST': #form has been submitted
        form = TargetForm(request.POST)
        if form.is_valid():
            form.save()  #save the data
            return HttpResponseRedirect('/targets/')
    else:
        form = TargetForm()
    return render(request, 'targets/addObject.html', {'form':form})


def targetList(request):
    '''return a list of targets and associeted information'''
    #TODO use content type negotiation to determine whether to return
    #json, html, or xml
    return render(request, 'targets/targetList.html',{'targets':Target.objects.all()})


def uploadCoordFile(request):
    '''upload a coordinate file for a target'''
    if request.method == 'POST':
        form = CoordFileModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/targets/')
    else:
        form = CoordFileModelForm()
    return render(request, 'targets/uploadCoordFile.html',{'form':form})

