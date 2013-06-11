# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.views.decorators.http import require_POST

import json


from models import Target, FieldObject
from forms import TargetForm, CoordFileModelForm, ShortTargetForm

@login_required
def index(request):
    '''index page, just view a list
    of targets in the database'''
    return HttpResponseRedirect('/targets/targetList/')

@login_required
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


@login_required
def targetList_html(request):
    '''return a list of targets and associeted information'''
    #TODO use content type negotiation to determine whether to return
    #json, html, or xml
    return render(request, 'targets/targetList.html',{'targets':Target.objects.all()})

@login_required
def targetList_json(request):
    '''return a json list of targets and associeated information'''
    targets = Target.objects.all()
    result = [ {'id':t.id, 'name':t.name, 'ra':str(t.ra),'dec':str(t.dec), 'simbadName':t.simbadName} for t in targets]
    return HttpResponse(json.dumps(result),mimetype='application/json')


@login_required
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


@login_required
def edit_targets(request):
    '''allow user to edit targets in database'''
    TargetFormset = modelformset_factory(Target,form=ShortTargetForm,can_delete=True)
    if request.method == 'POST':
        formset = TargetFormset(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = TargetFormset()
    return render(request, 'targets/edit_objs.html',{'formset':formset})

@login_required
def edit_fieldObjects(request):
    '''allow user to add and modify coordinates for field objects'''
    context = {
        'targets': Target.objects.all()
    }
    return render(request, 'targets/edit_fieldObjects.html',context)

@login_required
def coordlist_json(request, targetID=None):
    '''get a list of FieldObject objects in JSON
    for the given target id, if targetID is None, then
    return all FieldObjects'''
    if not targetID:
        objs = FieldObject.objects.all()
    else:
        objs = FieldObject.objects.filter(target_id=targetID)
    result = [{'id': t.id, 'ra':str(t.ra), 'dec':str(t.dec), 'isTarget':t.isTarget} for t in objs]
    return HttpResponse(json.dumps(result),mimetype='applicatin/json')
#TODO make view for coordlist_html


@login_required
@require_POST
def fieldObjectDelete(request,objID):
    '''perform some action for the FieldObject given by ID'''
    obj = get_object_or_404(FieldObject, pk=objID)
    obj.delete()
    return HttpResponse("Deleted {0}".format(objID))
        
