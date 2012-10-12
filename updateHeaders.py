#!/usr/bin/python

#updateHeaders.py
#
# functions to update certain headers for our frames

import obsDB
import frameTypes

import pyfits


def updateObjName(header):
	if 'object' in header:
		return 
	else:
		header['object'] = frameTypes.getObjectName(header)
		return
	
def updateImType(header):
	header['imagetyp']=frameTypes.getFrameType(header)
	return

def updateSubset(header):
	if 'filter' in header:
		header['subset']=header['filter']
		return
	else:
		return


def updateAll(header):
	updateObjName(header)
	updateImType(header)
	updateSubset(header)

def updateFrame(fname, replaceFname=None):
	'''Update the headers for a frame with the 
filename `fname'. if replaceFname is None, or not given, then
the new header overwrite the existing header, if replaceFname is given and not None, then a copy of the fits file is created with the new header'''
	with pyfits.open(fname) as fitsfile:
		updateAll(fitsfile[0].header)
		if replaceFname is not None:
			fitsfile.writeto(replaceFname)
		else:
			fitsfile.writeto(fname,clobber=True)
	return


	
