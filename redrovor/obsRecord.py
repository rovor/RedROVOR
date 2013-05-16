#!/usr/bin/python

import obsDB
import pyfits
import frameTypes
import re

from fitsHeader import isFits

import os

import logging
import traceback

logger = logging.getLogger("Rovor.recordobs")

dateRegex = re.compile(r'(\d{4}-\d{2}-\d{2})T.*')

def recordObservation(fitsHeader,fname=''):
    '''record the information contained in the header to the online database
    and optionally the filename passed as fname'''
    objName = frameTypes.getObjectName(fitsHeader)
    obj = obsDB.obj_get_or_add(objName)
    logger.info(obj)
    objid = obj['obj_id']
    ffilter = fitsHeader['FILTER']
    exptime = fitsHeader['EXPTIME']
    temp = fitsHeader['CCD-TEMP']
    utdate = dateRegex.match(fitsHeader['DATE-OBS']).group(1)

    obsDB.newObservation(objid,utdate,ffilter,exptime,temp,fname=os.path.realpath(fname))
    return

def recordDir(dir):
    '''record information for all fits files of images in 
    the given directory and subdirectories'''
    logger.info("Recording observations in "+dir)
    obsDB.login()
    for root, dirs, files in os.walk(dir):
        logger.info("root = "+root)
        for f in files:
            fullPath = os.path.join(root,f)
            if isFits(fullPath):
                #logger.info("Attempting to record observation for "+f)
                try:
                    header = pyfits.getheader(fullPath)
                    if frameTypes.getFrameType(header) != 'object':
                        continue
                    recordObservation(header,fullPath)
                except Exception as e:
                    logger.error(traceback.format_exc())
                    break #keep going and record everything else
