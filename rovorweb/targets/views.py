# Create your views here.

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.forms.models import modelformset_factory, modelform_factory
from django.forms.formsets import formset_factory
from django.views.decorators.http import require_POST
from django.db import transaction

import json

import logging

logger = logging.getLogger("Rovor")


from models import Target, FieldObject
from forms import TargetForm, CoordFileModelForm, ShortTargetForm

from redrovor.coords import parseCoords
from root.jsonresponse import okJSONResponse, errorJSONResponse

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
@require_POST
def uploadCoordFile(request,targetID):
    '''upload a coordinate file for a target'''
    try:
        f = request.FILES['coords']
        result = []
        with transaction.commit_on_success():
            for ra,dec in parseCoords(f):
                logger.info("Adding object at {0} {1}".format(ra,dec))
                obj = FieldObject(target_id=targetID,ra=ra,dec=dec,isTarget=False)
                obj.save()
                result.append(FieldObject2dict(obj))
        return okJSONResponse(result)
    except Exception as ex:
        return errorJSONResponse(str(ex))


@login_required
def edit_targets(request):
    '''allow user to edit targets in database'''
    TargetFormset = modelformset_factory(Target,form=ShortTargetForm,can_delete=True)
    if request.method == 'POST':
        formset = TargetFormset(request.POST)
        if formset.is_valid():
            formset.save()
            formset = TargetFormset() #reset form so we have the updated form
    else:
        formset = TargetFormset()
    return render(request, 'targets/edit_objs.html',{'formset':formset})

@login_required
def edit_fieldObjects(request):
    '''allow user to add and modify coordinates for field objects'''
    context = {
        'targets': Target.objects.all(),
        'addForm': modelform_factory(FieldObject)
    }
    return render(request, 'targets/edit_fieldObjects.html',context)


def FieldObject2dict(fieldobject):
    '''get a dict representing the fieldobject, so that it  is
    easier to convert it to JSON'''
    return {'id':fieldobject.id, 'ra':str(fieldobject.ra), 'dec':str(fieldobject.dec), 'isTarget':fieldobject.isTarget}

@login_required
def coordlist_json(request, targetID=None):
    '''get a list of FieldObject objects in JSON
    for the given target id, if targetID is None, then
    return all FieldObjects'''
    if not targetID:
        objs = FieldObject.objects.all()
    else:
        objs = FieldObject.objects.filter(target_id=targetID)
    result = [FieldObject2dict(t) for t in objs]
    logger.debug("result: {0}".format(result))
    return HttpResponse(json.dumps(result),mimetype='applicatin/json')
#TODO make view for coordlist_html



@login_required
@require_POST
def fieldObjectDelete(request,objID):
    '''perform some action for the FieldObject given by ID'''
    obj = get_object_or_404(FieldObject, pk=objID)
    obj.delete()
    return HttpResponse("Deleted {0}".format(objID))
        
@login_required
@require_POST
def fieldObjectAdd(request):
    '''add a field object to the database'''
    FOForm = modelform_factory(FieldObject,fields=['target','ra','dec','isTarget'])
    form = FOForm(request.POST)
    if form.is_valid():
        obj = form.save()
        return okJSONResponse({'id':obj.id, 'ra':str(obj.ra),'dec':str(obj.dec), 'isTarget':obj.isTarget})
    else:
        return errorJSONResponse(form.errors)

@login_required
@require_POST
def fieldObjectAddTarget(request):
    '''add the target object to the list of coordinates for that target'''
    try:
        targ = Target.objects.get(pk=request.POST['target'])
        fobj = FieldObject(target=targ, ra=targ.ra, dec=targ.dec,isTarget=True)
        fobj.save() 
        return okJSONResponse(FieldObject2dict(fobj))
    except Exception as e:
        logger.debug(e)
        return errorJSONResponse("targetID must be supplied and a valid target")

@login_required
@require_POST
def synchronizeTargets(request):
    '''synchronize the targets database with rovor.byu.edu'''
    Target.synchronize()
    return okJSONResponse()
