'''This is just a helper module to factor out the actions of reduction from the actual pages, everything in here is imported into the main views module'''


from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import json
import os

from redrovor import renamer
from redrovor.process import makeZero
from redrovor.zerodarkprocess import ZeroDarkProcessor, doFirstPass
from redrovor.secondpass import SecondPassProcessor, doSecondPass
from dirmanage.models import Filesystem

import logging
logger = logging.getLogger('Rovor')

from dirmanage.toolset import process_path


@login_required
def renameAll(request):
    '''rename all files in a folder to be .fit instead of .FIT'''
    def rename_func(path):
        renamer.renameAll(path) #rename the files
        return None
    return process_path(request,rename_func)


@login_required
def makeZero(request):
    '''make a master zero from a folder'''
    def zmaker(path):
        improc = ZeroDarkProcessor(path)
        logger.info("Making zero at path " + path)
        improc.makeZero()
        return None
    return process_path(request,zmaker)

@login_required
def makeDark(request):
    '''make a master dark from a folder'''
    def dmaker(path):
        improc = ZeroDarkProcessor(path)
        logger.info("Making dark at path " + path)
        improc.makeDark()
        return None
    return process_path(request,dmaker)

@login_required
def makeFlats(request):
    '''make master flats from a folder'''
    def fmaker(path):
        improc = ZeroDarkProcessor(path)
        logger.info("Making flats at path " + path)
        improc.makeFlats()
        return None
    return process_path(request,fmaker)

@login_required
def subZeroDark(request):
    '''subtract zeros and darks from the object files in a folder'''
    def subber(path):
        improc = ZeroDarkProcessor(path)
        logger.info("Processing object files in "+path)
        improc.zero_and_dark_subtract()
        return None
    return process_path(request,subber)

@login_required
def firstPass(request):
    '''perform the first pass over the folder
    i.e. create calibration frames and apply zeros 
    and darks to the object frames, and save them in the processed folder
    '''
    return process_path(request, doFirstPass)


def applyFlats(request):
    '''apply the given flats to the supplied path'''
    def applier(path):
        flats = json.loads(request.POST['flats'])
        for filt,flat in flats.items():
            flats[filt] = Filesystem.getTruePath(flat)
        improc = SecondPassProcessor(path)
        improc.applyFlats(flats)
    return process_path(request,applier)

def applyWCS(request):
    '''apply world coordinate system to 
    images'''
    def applier(path):
        improc = SecondPassProcessor(path)
        improc.applyWCS()
    return process_path(request,applier)

def secondPass(request):
    '''perform the second pass over the folder
    i.e. apply flats and apply world coordinate system
    '''
    return process_path(request,doSecondPass)
        
    
        


