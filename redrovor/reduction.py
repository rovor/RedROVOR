#!/usr/bin/python

import sys
import datetime
import os
import os.path as path
import shutil
import tempfile

import logging

from glob import glob
from collections import defaultdict

import pyfits

import updateHeaders
import frameTypes
import process
#import imProc
import coords

from utils import writeListToFileName

#TODO allow more flexibility in where the output files are stored
ProcessedFolderBase = '/data/Processed'
MasterCalFolder = '/data/Calibration'



def genDate(date):
    return date.strftime('/%Y/%b/%d%b%Y').lower()


def createResultFolder(date):
    '''given a datetime.date create a new folder to hold the resulting 
processed images.'''
    folderName = ProcessedFolderBase+genDate(date)
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

        # set up logger
        self.logger = logging.getLogger('Rovor.ImProcessor_{0}'.format(id(self)))

        self.rawFolder = rawFolder
        #TODO figure out a robust way to determine the date of observation
        #for now we will simply look at the date of observation for the first
        #fits file
        
        self._findFrames()  #find frames
        header = pyfits.getheader(self.frames[0])
        self.obsDate = datetime.datetime.strptime(header['date-obs'],'%Y-%m-%dT%H:%M:%S.%f').date()
        #create the folder to store results in
        self.processedFolder = createResultFolder(self.obsDate)


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
    def _findFrames(self):
        '''find  all fits files in the folder (anything ending with .fits, .fit, .FIT, or .fts'''
        self.logger.info('Looking for frames...')
        validExtensions = ['.fits','.fit','.FIT','.fts']
        self.frames=list()
        for ext in validExtensions:
            self.frames.extend( glob(self.rawFolder+'/*'+ext) )
        return self
    def updateHeaders(self,inplace=True):
        '''update the headers for all the frames in the folder
always works in place'''
        self.logger.info('Updating Headers...')
        for frame in self.frames:
            updateHeaders.updateFrame(frame)
        return self
    def buildLists(self):
        self.logger.info("Building Lists")
        self.frameTypes = frameTypes.getFrameLists( self.frames ) #get frame types
        self.objects = frameTypes.makeObjectMap( self.frameTypes['object'] )
        self.logger.info("Saving frame lists to files")
        frameTypes.saveFrameLists(self.frameTypes,zeroFile=self.zerosFile, darkFile=self.darksFile,
            flatFile=self.flatsFile, objectFile=self.objectsFile,unknownFile=self.unknownFile) 
        return self
    def makeZero(self):
        #insure that we have the frame types already
        if not self.frameTypes:
            self.logger.warning('Type lists were not previously made, making them now')
            self.buildLists()
        self.logger.info('Making Zero')
        self.zeroFrame = path.join(self.processedFolder, 'Zero.fits')
        self.logger.info("Set zeroFrame to "+ self.zeroFrame)
        process.makeZero(*self.frameTypes['zero'], output=self.zeroFrame)
        return self
    def ensure_zero(self):
        '''check to see if we already have a zeroFrame location, 
        if not look for a zero in the processed folder, if we still can't find one
        then run makeZero'''
        self.zeroFrame = self.zeroFrame or path.join(self.processedFolder, 'Zero.fits')
        if not path.isfile(self.zeroFrame):
            #the zero hasn't been made yet
            self.makeZero()
    def makeDark(self):
        self.logger.info('Making Dark')
        self.ensure_zero()  #make sure we have a zero to use
        self.darkFrame = path.join(self.processedFolder,'Dark.fits')
        #apply zeros to darks
        process.makeDark(*self.frameTypes['dark'],zero=self.zeroFrame,output=self.darkFrame)
        return self
    def ensure_dark(self):
        '''check to see if we already have a zeroFrame location, 
        if not look for a zero in the processed folder, if we still can't find one
        then run makeZero'''
        self.darkFrame = self.darkFrame or path.join(self.processedFolder, 'Dark.fits')
        if not path.isfile(self.darkFrame):
            #the dark hasn't been made yet
            self.makeDark()
    def makeFlats(self):
        self.logger.info('Making Flats')
        self.logger.warning('Operations on flats have not been finished yet')
        self.ensure_frameTypes()
        self.ensure_zero()
        self.ensure_dark()
        flatBase = path.join(self.processedFolder,'Flat')
        flats = frameTypes.splitByFilter(self.frameTypes['flat'])
        self.flatFrames = {}
        for filter in flats:
            outName = "{0}_{1}.fits".format(flatBase,filter)  #name is the base flat name plus the filter type
            process.makeFlat(*flats[filter],zero=self.zeroFrame,dark=self.darkFrame,output=outName)
            self.flatFrames[filter] = outName
        #TODO should we copy the flats to calibration folder?
        return self

        
    def imProc(self, useFlats=False):
        '''process the image frames'''
        self.logger.info('Processing Images...')
        if not self.flatList and useFlats:
            self.makeFlats()
        self.newObjs = defaultdict(list)
        for (obj,flist) in self.objects.items():
            #iterate over each object
            count=0
            for frame in flist:
                newName = "{0}/{1}-{2}.fits".format(self.processedFolder,obj.replace(' ','_'),count)
                #imProc.processImages(frame,imProc.INPUT_SINGLEFRAME,output=newName,zero=self.zeroFrame,dark=self.darkFrame,
                    #flat=','.join(self.flatList))
                self.newObjs[obj].append(newName)
                #now apply world coordinates
                coords.astrometrySolve(newName)
                #increment counter
                count+=1
            writeListToFileName(self.newObjs[obj], path.join(self.processedFolder, "object_{0}.lst".format(obj)))

    def process(self, doFlats=False):
        '''process everything in the folder and put the new frames in the new folder'''
        self.logger.info('Processing Directory...')
        self.updateHeaders()
        self.buildLists()
        self.makeZero()
        self.makeDark()
        self.makeFlats()
        if doFlats:
            self.imProc(useFlats=doFlats)
        else:
            self.logger.info('Not doing final image calibration\nbecause we don\'t know what flats to use')

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
