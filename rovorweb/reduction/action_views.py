'''This is just a helper module to factor out the actions of reduction from the actual pages, everything in here is imported into the main views module'''


from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
import os
import traceback

from redrovor import renamer
from redrovor.process import makeZero
from redrovor.firstpass import FirstPassProcessor, doFirstPass
from redrovor.secondpass import SecondPassProcessor, doSecondPass
from redrovor.thirdpass import ThirdPassProcessor, doThirdPass
from dirmanage.models import Filesystem
from dirmanage.toolset import PathProcessView, process_path

from root.jsonresponse import okJSONResponse, errorJSONResponse

import logging
logger = logging.getLogger('Rovor')



@login_required
@PathProcessView.pathOnly
def renameAll(path):
    '''rename all files in a folder to be .fit instead of .FIT'''
    renamer.renameAll(path) #rename the files
    return okJSONResponse()


@login_required
@PathProcessView.pathOnly
def makeZero(path):
    '''make a master zero from a folder'''
    try:
        improc = FirstPassProcessor(path)
        logger.info("Making zero at path " + path)
        improc.makeZero()
        return okJSONResponse()
    except ValueError as e:
        return errorJSONResponse(str(e))
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e

@login_required
@PathProcessView.pathOnly
def makeDark(path):
    '''make a master dark from a folder'''
    try:
        improc = FirstPassProcessor(path)
        logger.info("Making dark at path " + path)
        improc.makeDark()
        return okJSONResponse()
    except ValueError as e:
        return errorJSONResponse(str(e))
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e

@login_required
@PathProcessView.pathOnly
def makeFlats(path):
    '''make master flats from a folder'''
    try:
        improc = FirstPassProcessor(path)
        logger.info("Making flats at path " + path)
        improc.makeFlats()
        return okJSONResponse()
    except ValueError as e:
        return errorJSONResponse(str(e))
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e

@login_required
@PathProcessView.pathOnly
def subZeroDark(path):
    '''subtract zeros and darks from the object files in a folder'''
    try:
        improc = FirstPassProcessor(path)
        logger.info("Processing object files in "+path)
        improc.zero_and_dark_subtract()
        return okJSONResponse()
    except ValueError as e:
        return errorJSONResponse(str(e))
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e

@login_required
@PathProcessView.pathOnly
def firstPass(path):
    '''perform the first pass over the folder
    i.e. create calibration frames and apply zeros 
    and darks to the object frames, and save them in the processed folder
    '''
    try:
        doFirstPass(path)
        return okJSONResponse()
    except ValueError as e:
        return errorJSONResponse(str(e))
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e
        

@login_required
@PathProcessView.decorate
def applyFlats(request,path):
    '''apply the given flats to the supplied path'''
    try:
        flats = json.loads(request.POST['flats'])
        for filt,flat in flats.items():
            flats[filt] = Filesystem.getTruePath(flat)
        improc = SecondPassProcessor(path)
        improc.applyFlats(flats)
        return okJSONResponse()
    except ValueError as e:
        return errorJSONResponse(str(e))
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e

@login_required
@PathProcessView.pathOnly
def applyWCS(path):
    '''apply world coordinate system to 
    images'''
    try:
        improc = SecondPassProcessor(path)
        improc.applyWCS()
        return okJSONResponse()
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e

@login_required
@PathProcessView.decorate
def secondPass(request,path):
    '''perform the second pass over the folder
    i.e. apply flats and apply world coordinate system
    '''
    try:
        if 'flats' not in request.POST:
            return HttpResponseBadRequest("No flats specified")
        flats = json.loads(request.POST['flats'])
        for filt,flat in flats.items():
            flats[filt] = Filesystem.getTruePath(flat)
        doSecondPass(path,flats)
        return okJSONResponse()
    except ValueError as e:
        return errorJSONResponse(str(e))
    except Exception as e:
        #an unexpected exception
        logger.debug(traceback.format_exc()) #log the traceback
        raise e
        
@login_required
@require_POST
def thirdPass(request):
    '''web service to perform the photometry'''
    #the mapping object has rather sensitive information in it
    #so we don't want the client to deal with it, so we need to
    #have everything in the session
    path = request.session.get('phot.path')
    mapping = request.session.get('phot.object_mapping')
    if path and mapping:
        #clean up session
        del request.session['phot.path'] 
        del request.session['phot.object_mapping'] 
    else:
        return HttpResponseBadRequest("No mapping specified")
    try:
        doThirdPass(path,mapping)
    except Exception as e:
        logger.debug(traceback.format_exc())
        return errorJSONResponse(str(e))
    finally:
        #clean up all the temporary files
        # we need to do this no matter what
        for tempFile, _ in mapping.values():
            os.remove(tempFile)
    return okJSONResponse()

@login_required
@PathProcessView.decorate
def photSelectFolder(request,path):
    '''Allows a client to select a path for performing,
    photometry. The client must supply the paramater 'path',
    which is the virtual path to the folder to perform photometry in,
    and will receive a Json object which contains an object of the following form
        ok: True if the request succeeded
        error: the error message if ok is false, not present if ok is true
        result: the response if ok is true, not present if ok is false, it will be a list
            of objects that do not have coordinates for them, if all objects have coordinates it will
            be an empty list.
    It is up to the client whether to continue forward or not if there are missing coordinates, the client
    can also use the targets API to upload more coordinates.'''
    try:
       mapping, missing = getObjectMapping(path)
       request.session['phot.object_mapping'] = mapping
       request.session['phot.path'] = path
       return okJSONResponse(missing)
    except Exception as e:
        logger.debug(traceback.format_exc())
        return errorJSONResponse(str(e))
