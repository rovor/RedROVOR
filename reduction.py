#!/usr/bin/python

import sys
import datetime
import os
import os.path as path
import shutil
import tempfile
from glob import glob
from collections import defaultdict

import pyfits

import updateHeaders
import frameTypes
import imProc
import coords

from rovUtils import writeListToFileName

ProcessedFolderBase = '/data/Processed'
MasterCalFolder = '/data/Calibration'


def createResultFolder(date):
	'''given a datetime.date create a new folder to hold the resulting 
processed images.'''
	folderName = ProcessedFolderBase+date.strftime('/%Y/%b/%d%b%Y').lower()
	if not path.isdir(folderName):
		os.makedirs(folderName)  #create folder in format ddmonyyyy inside folder for month inside folder for year
	return folderName

def relocateFiles(fileList, destFolder):
	'''takes a list of filenames (fileList) and adds the destFolder to the beginning of them, returning a new list'''
	return [ path.join(destFolder, path.basename(fname)) for fname in fileList ]

class ImProcessor:
	'''Class to handle image processing for a folder, we use a class to 
make it easier to keep track of the state'''

	def __init__(self, rawFolder):
		'''initialize the processor in the folder containing the raw data'''
		self.rawFolder = rawFolder
		#TODO figure out a robust way to determine the date of observation
		#for now we will simply look at the date of observation for the first
		#fits file
		
		#create the folder to store results in
		header = pyfits.getheader(glob(path.join(rawFolder,'*.fits'))[0])
		self.obsDate = datetime.datetime.strptime(header['date-obs'],'%Y-%m-%dT%H:%M:%S.%f').date()
		self.processedFolder = createResultFolder(self.obsDate)
		self.findFrames()
		self.zeroFrame = None
		self.zerosFile = path.join(self.rawFolder, 'zeroFrames.lst')
		self.darkFrame = None
		self.darksFile = path.join(self.rawFolder, 'darkFrames.lst')
		self.flatBase = None
		self.flatList =  []
		self.flatsFile = path.join(self.rawFolder, 'flatFrames.lst')
		self.frameTypes = None
		self.objects = None
		self.objectsFile = path.join(self.rawFolder, 'objectFrames.lst')
		self.unknownFile = path.join(self.rawFolder, 'unknownFrames.lst')
		return
	def findFrames(self):
		'''find  all fits files in the folder (anything ending with .fits, .fit, .FIT, or .fts'''
		validExtensions = ['.fits','.fit','.FIT','.fts']
		self.frames=list()
		for ext in validExtensions:
			self.frames.extend( glob(self.rawFolder+'/*'+ext) )
		return self
	def updateHeaders(self,inplace=True):
		'''update the headers for all the frames in the folder
always works in place'''
		for frame in self.frames:
			updateHeaders.updateFrame(frame)
		return self
	def buildLists(self):
		self.frameTypes = frameTypes.getFrameLists( self.frames ) #get frame types
		self.objects = frameTypes.makeObjectMap( self.frameTypes['object'] )
		frameTypes.saveFrameLists(self.frameTypes,zeroFile=self.zerosFile, darkFile=self.darksFile,
			flatFile=self.flatsFile, objectFile=self.objectsFile,unknownFile=self.unknownFile) 
		return self
	def makeZero(self):
		#insure that we have the frame types already
		if not self.frameTypes:
			self.buildLists()
		self.zeroFrame = path.join(self.processedFolder, 'Zero.fits')
		imProc.makeZero(self.zerosFile, imProc.INPUT_LISTFNAME, output=self.zeroFrame)
		return self
	def makeDark(self):
		if not self.zeroFrame:
			self.makeZero()
		self.darkFrame = path.join(self.processedFolder,'Dark.fits')
		processedDarks = relocateFiles(self.frameTypes['dark'],self.processedFolder)
		processedDarksFile = path.join(self.processedFolder, 'darksProcd.lst')
		writeListToFileName(processedDarks,processedDarksFile )
		#apply zeros to darks
		imProc.processImages(self.darksFile,imProc.INPUT_LISTFNAME,output=processedDarksFile,outputType=imProc.INPUT_LISTFNAME,
			zerocor=imProc.yes,darkcor=imProc.no,flatcor=imProc.no,ccdtype='dark',zero=self.zeroFrame)
		#create the dark frame
		imProc.makeDark(processedDarksFile,imProc.INPUT_LISTFNAME, output=self.darkFrame,process=imProc.no) 
		return self
	def makeFlats(self):
		if not self.darkFrame:
			self.makeDark()
		self.flatBase = path.join(self.processedFolder,'Flat')
		processedFlats = relocateFiles(self.frameTypes['flat'],self.processedFolder)
		processedFlatsFile = path.join(self.processedFolder, 'flatsProcd.lst')
		if not processedFlats:
			#there aren't any flats to process
			#use the most recent master flats
			self.flatlist=glob(path.join(masterCalFolder,'Flat*'))
			return self
		writeListToFileName(processedFlats, processedFlatsFile)
		#apply zeros and darks to flats
		imProc.processImages(self.flatsFile,imProc.INPUT_LISTFNAME,output=processedFlatsFile, outputType=imProc.INPUT_LISTFNAME, zerocor=imProc.yes,darkcor=Improc.yes,
			flatcor=imProc.no,ccdtype='flat',zero=self.zeroFrame, dark=self.darkFrame)
		#create the zeros
		imProc.makeFlats(processedFlatsFile,imProc.INPUT_LISTFNAME, output=self.flatBase,process=imProc.no)

		#copy flats to the master flats folder
		self.flatList = glob(path.join(self.processedFolder,'Flat*'))
		for flat in self.flatList:
			shutil.copy(flat,path.join(MasterCalFolder,path.basename(flat)))
		
	def imProc(self, useFlats=False):
		'''process the image frames'''
		if not self.flatList and useFlats:
			self.makeFlats()
		self.newObjs = defaultdict(list)
		for (obj,flist) in self.objects.items():
			#iterate over each object
			count=0
			for frame in flist:
				newName = "{0}/{1}-{2}.fits".format(self.processedFolder,obj.replace(' ','_'),count)
				imProc.processImages(frame,imProc.INPUT_SINGLEFRAME,output=newName,zero=self.zeroFrame,dark=self.darkFrame,
					flat=','.join(self.flatList))
				self.newObjs[obj].append(newName)
				#now apply world coordinates
				coords.astrometrySolve(newName)
				#increment counter
				count+=1
			writeListToFileName(self.newObjs[obj], path.join(self.processedFolder, "object_{0}.lst".format(obj)))

					
	def process(self, doFlats=False):
		'''process everything in the folder and put the new frames in the new folder'''
		self.findFrames()
		self.updateHeaders()
		self.buildLists()
		self.makeZero()
		self.makeDark()
		if doFlats:
			self.makeFlats()
		self.imProc(useFlats=doFlats)

if __name__ == '__main__':
	#optparse is deprecated after python 2.7, but
	#argparse isn't available on python 2.6, which is what
	#we are currently using, if we upgrade to a newer version
	#of python then we should change to argparser

	from optparse import OptionParser
	parser = OptionParser()

	parser.add_option('-F', '--use-flats', action='store_true', dest='useFlats', default=False, help='apply flats when doing the calibration (not done by default because flats can be tricky)')
	
	(options,args)=parser.parse_args()
	if  len(args) != 1:
		parser.error("incorrect number of arguments")
	rawDirectory = args[0]
	processor = ImProcessor(rawDirectory)
	processor.process(doFlats=options.useFlats)
