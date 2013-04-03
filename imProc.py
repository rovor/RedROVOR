#!/usr/bin/python

#imProc.py 
#
# functions to wrap IRAF so to process frames, and apply calibration frames

from pyraf import iraf

yes= iraf.yes
no =iraf.no
#load relevant packages

iraf.noao()
iraf.imred()
iraf.ccdred()


#constants for input types
INPUT_PYLIST=1 #a python list of files
INPUT_SINGLEFRAME=2 #a string containing the name of a single frame
INPUT_STRLIST=3 #a string containing comma delimited frames, or an IRAF expression that generates a list
INPUT_LISTFNAME=4 #a string containing the name of a file which has a list of the frames to process
INPUT_GLOB=5 #a globbing expression, glob evaluated with shell

def _genIRAFString(fileList, inputType):
	'''convert fileList to a valid string for input to IRAF tasks. fileList is either a string or (for inputType=INPUT_PYLIST) a python list. The way it is interpreted is dependent on the value of inputType which should be one of the constants above [INPUT_PYLIST, INPUT_SINGLEFRAME, INPUT_STRLIST, INPUT_LISTFNAME, and INPUT_GLOB] at the moment INPUT_STRLIST and INPUT_SINGLEFRAME behave identically. '''
	if inputType == INPUT_LISTFNAME:
		return '@'+fileList
	elif inputType == INPUT_SINGLEFRAME or inputType == INPUT_STRLIST:
		return fileList
	elif inputType == INPUT_PYLIST:
		return ','.join(fileList)
	elif  inputType == INPUT_GLOB:
		return ','.join(glob.glob(fileList))
	else:
		raise ValueError('{0} is not a vlid inputType'.format(inputType))
	return

def makeZero(fileList='zeros.lst',inputType=INPUT_LISTFNAME,output="Zero.fits",combine='average',reject='minmax',ccdtype='zero'):
	'''create a master Zero.fits from the frames in fileList'''
	iraf.zerocombine(_genIRAFString(fileList,inputType),output=output,combine=combine,reject=reject,ccdtype=ccdtype)
	print "zerocombine successful"
	return

def makeDark(fileList='darks.lst',inputType=INPUT_LISTFNAME,output='Dark.fits',process=iraf.yes,combine='average',ccdtype='dark',reject='minmax'):
	'''create a master Dark.fits from the  darks in fileList'''
	iraf.darkcombine(_genIRAFString(fileList,inputType), output=output, combine=combine, process=process,ccdtype=ccdtype,reject=reject)

def makeFlat(fileList='flats.lst',inputType=INPUT_LISTFNAME, output='Flat',combine='average',
	reject='avsigclip', ccdtype='flat', process = iraf.yes, subsets=iraf.yes, scale='mode'):
	'''create master Flats from fileList, if subsets is iraf.yes, then
	create a different flat for each subset indicated in the subset header'''
	iraf.flatcombine(_genIRAFString(fileList, inputType), output=output,
		combine=combine, process=process, ccdtype=ccdtype,reject=reject, scale=scale, subsets=subsets)
	return

def processImages(fileList, inputType=INPUT_SINGLEFRAME, output="",outputType=INPUT_SINGLEFRAME, ccdtype="object", zerocor= iraf.yes, darkcor=iraf.yes, flatcor=iraf.yes, zero="Zero.fits",dark="Dark.fits", flat="Flat*.fits"):
	'''wrapper for IRAF's ccdproc command'''
	iraf.ccdproc(_genIRAFString(fileList, inputType), output=_genIRAFString(output,outputType), ccdtype=ccdtype, zerocor = zerocor, 
	darkcor=darkcor, flatcor=flatcor, zero=zero, dark=dark, flat=flat,
	fixpix=iraf.no,overscan=iraf.no,trim=iraf.no)
	return

	
	
