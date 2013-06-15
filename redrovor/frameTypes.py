#!/usr/bin/python

import pyfits

import sys
import os
import os.path
from collections import defaultdict

import obsDB
from fitsHeader import isFits, getFrameType, getObjectName, splitByHeader


def getFrameLists(fileList):
	'''given an iterator of filenames, go through each one, 
	get the the type of the frame and add it to the appropriate list
	return a dictionary containing lists of files for 'zero', 'dark',
	'object', and 'none'. The 'none' category will contain fits files
	that we can't determine the type for and files that we are unable to 
	open'''
	results = {'zero':[],'dark':[],'flat':[],'object':[],'unknown':[]}
	for f in iter(fileList):
		try:
			imType = getFrameType(pyfits.getheader(f))
		except:
			imType = 'unknown'	
		if imType is None:
			imType = 'unknown'
		results[imType].append(f)
	return results

def saveFrameLists(frameLists, zeroFile='zeros.lst',darkFile='darks.lst',
	flatFile='flats.lst',objectFile='objects.lst',unknownFile='unknown.lst'):
	'''Take the output from getFrameLists, and save them to files'''
	with open(zeroFile,'w') as zf:
		for frame in frameLists['zero']:
			zf.write('{0}\n'.format(frame))
	with open(darkFile,'w') as df:
		for frame in frameLists['dark']:
			df.write('{0}\n'.format(frame))
	with open(flatFile,'w') as ff:
		for frame in frameLists['flat']:
			ff.write('{0}\n'.format(frame))
	with open(objectFile,'w') as of:
		for frame in frameLists['object']:
			of.write('{0}\n'.format(frame))
	with open(unknownFile,'w') as uf:
		for frame in frameLists['unknown']:
			uf.write('{0}\n'.format(frame))

def makeObjectMap(files):
	'''create a dictionary with keys of the objects, and
	   the values are lists of all the frames of that object
	'''
	result = defaultdict(list)
	for frame in iter(files):
		result[getObjectName(pyfits.getheader(frame))].append(frame)
	return result
	

def makeObjectList(files):
	'''create a list of all the objects observed'''
	return makeObjectMap(files).keys()

def printObjectList(objectlist,objectFile='objectList.lst'):
	'''create a file containing a list of all the objects in objectlist'''
	with open(objectFile,'w') as of:
		for obj in iter(objectlist):
			of.write(obj)
			of.write('\n')
	return

def printObjectMaps(objectMap, fileBase='obj_',ext='.lst'):
	'''for each object create file named fileBase+objName+ext 
	which contains a single line header in the formate #(objname) 
	followed a list of the frames of that object, one per line'''
	for obj, frames in objectMap.items():
		fname = fileBase + obj + ext #build name for the file
		with open(fname,'w') as olist:
			olist.write('#({0})\n'.format(obj)) #write header with object name
			for frame in frames:
				olist.write(frame)
				olist.write('\n')
	return


#main function
def main(fileList=None):
	if fileList is None:
		#default to everything in the folder
		fileList = os.listdir('.')	
	#look at the frame types
	frameTypes = getFrameLists(fileList)
	#get object names
	objNames = makeObjectMap(frameTypes['object'])
	
	#now print out the files
	printObjectMaps(objNames)
	printObjectList(objNames.keys())
	saveFrameLists(frameTypes) 
	
	
	
	
#run main if the script is directly executed
if __name__ == '__main__':
	main(sys.argv[1:])
	
