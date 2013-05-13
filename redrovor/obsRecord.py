#!/usr/bin/python

import obsDB
import pyfits
import frameTypes
import re

import os

dateRegex = re.compile(r'(\d{4}-\d{2}-\d{2})T.*')

def recordObservation(fitsHeader,fname=''):
	'''record the information contained in the header to the online database
	and optionally the filename passed as fname'''
	objName = frameTypes.getObjectName(fitsHeader)
	obj = obsDB.obj_get_or_add(objName)
	objid = obj['id']
	ffilter = fitsHeader['FILTER']
	exptime = fitsHeader['EXPTIME']
	temp = fitsHeader['CCD-TEMP']
	utdate = dateRegex.match(fitsHeader['DATE-OBS']).group(1)
	
	obsDB.newObservation(objid,utdate,ffilter,exptime,temp,fname=fname)
	return

def recordDir(dir):
	'''record information for all fits files of images in 
	the given directory and subdirectories'''
	for root, dirs, files in os.walk(dir):
		for f in files:
			if frameTypes.isFits(f):
                try:
                    header = pyfits.getheader(f)
                    if frameTypes.getFrameType(header) != 'object':
                        continue
                    recordObservation(header,f)
                except Exception as e:
                    #TODO: log error
                    continue #keep going and record everything else
				
