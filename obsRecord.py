#!/usr/bin/python

import obsDB
import pyfits
import frameTypes
import re

dateRegex = re.compile(r'(\d{4}-\d{2}-\d{2})T.*')

recordObservation(fitsHeader,fname=''):
	'''record the information contained in the header to the online database
	and optionally the filename passed as fname'''
	objName = frameTypes.getObjectName(fitsHeader)
	objs = obsDB.obj_search(objName) # search for object in database
	if not objs:
		objid = obsDB.addObject(objName)['id']  # add the object to database
	else:
		objid = objs[0]['id']
	ffilter = fitsHeader['filter']
	exptime = fitsHeader['exptime']
	temp = fitsHeader['CCD-TEMP']
	utdate = dateRegex.match(fitsHeader['DATE-OBS']).group(1)
	
	obsDB.newObservation(objid,utdate,ffilter,exptime,temp,fname=fname)
	return
