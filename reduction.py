#!/usr/bin/python

import datetime
import os
from glob import glob

ProcessedFolderBase = '/media/DATAPART1'


def createResultFolder(date):
	'''given a datetime.date create a new folder to hold the resulting 
processed images.'''
	folderName = ProcessedFolderBase+date.strftime('/%Y/%b/%d%b%Y').lower()
	os.makedirs(folderName)  #create folder in format ddmonyyyy inside folder for month inside folder for year
	return folderName

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
		return
		
