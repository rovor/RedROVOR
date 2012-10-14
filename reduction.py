#!/usr/bin/python

import datetime
import os.path as path
from os import path 
from glob import glob

import updateHeaders
import frameTypes
import imProc

ProcessedFolderBase = '/media/DATAPART1'


def createResultFolder(date):
	'''given a datetime.date create a new folder to hold the resulting 
processed images.'''
	folderName = ProcessedFolderBase+date.strftime('/%Y/%b/%d%b%Y').lower()
	os.makedirs(folderName)  #create folder in format ddmonyyyy inside folder for month inside folder for year
	return folderName

def relocateFiles(fileList, destFolder):
	'''takes a list of filenames (fileList) and adds the destFolder to the beginning of them, returning a new list'''
	return [ path.join(destFolder, fname) for fname in fileList ]

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
		header = pyfits.getheader(glob('*.FIT')[0])
		self.obsDate = datetime.datetime.strptime(header['date-obs'],'%Y-%m-%dT%H:%M:%S.%f').date()
		self.processedFolder = createResultFolder(self.obsDate)
		self.findFrames()
		self.zeroFrame = None
		self.darkFrame = None
		self.FlatList =  None
		self.frameTypes = None
		self.objects = None
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
		return self
	def makeZero(self):
		#insure that we have the frame types already
		if not self.frameTypes:
			self.buildLists()
		
		self.zeroFrame = path.join(self.processedFolder, 'Zero.fits')
		imProc.makeZero(self.frameTypes['zero'], INPUT_PYLIST, output=self.zeroFrame)
		return self
	def makeDark(self):
		if not self.zeroFrame:
			self.makeZero()
		self.darkFrame = path.join(self.processedFolder,'Dark.fits')
		processedDarks = relocateFiles(self.frameTypes['dark'],self.processedFolder)
		#apply zeros to darks
		imProc.processImages(self.frameTypes['dark'],INPUT_PYLIST,output=processedDarks),
			zerocor=imProc.yes,darkcor=imProc.no,flatcor=imProc.no,ccdtype='dark',zero=self.zeroFrame)
		#create the dark frame
		imProc.makeDark(self.frameTypes['dark'],INPUT_PYLIST, output=self.darkFrame,process=imProc.no) 
		return self
