'''module for code to perform the second pass, which consists of:
    * Apply Flats
    * Apply WCS to images
    
NOTE: we may change the name of this module at a later time'''

import logging
import json
import pyfits
from os import path

import observatories

from utils import findFrames
from frameTypes import getFrameLists 
from fitsHeader import getRA, getDec, splitByHeader
from wcs import astrometrySolve

from process import applyFlat

import renamer


class SecondPassProcessor:
    '''Class for taking care of all the processing needed for 
    the second pass. Again the name may change, but I couldn't 
    think of a good name since Flats and WCS coordinates don't 
    have a lot in common except that we are going to do them at 
    the same time'''

    def __init__(self,folder):
        '''initalize the class with the path of the folder that we are going to process.
        This path will mostly be a subdirectory of the Processed folder'''
        self.folder = folder
        self.logger =  logging.getLogger("Rovor.secondpass")
        self.objects = None
    def buildObjectList(self):
        self.logger.info("Building Object List")
        frames = findFrames(self.folder)
        frameTypes = getFrameLists( frames ) #get frame types
        self.objects = splitByHeader(frameTypes['object'],'filter')
        #save a cache of the frame info to speed up future uses of the ZeroDarkProcessor
        with open(path.join(self.folder,'objectLists.json'),'w') as f:
            json.dump(self.objects,f)
        return self
    def ensure_objectList(self):
        '''ensure that frameTypes is set'''
        if not self.objects:
            objectPath = path.join(self.folder,'objectLists.json')
            #if we have a previously made file load that
            if path.isfile(objectPath):
                with open(objectPath,'r') as f:
                    self.objects = json.load(f)
            else: #otherwise build the lists
                self.logger.warning('Object lists were not previously made, making them now')
                self.buildObjectList()
    def neededFilters(self):
        '''get the filters that the object frames are in so that we know which filters we need to use for
        flat processing, returns a set'''
        self.ensure_objectList()
        return list(self.objects.keys())
    def applyFlats(self,flatDict):
        '''@brief Apply Flats in \p flatdict to object images in the folder

        For each flat in the dictionary flatDict apply the flats to all object
        images in that filter

        @param[in] flatDict a dictionary mapping the names of filters to paths
        of the flat to use for that filter
        @returns self
        '''
        self.logger.info("Applying Flats to "+self.folder)
        self.ensure_objectList()
        for filt,flat in flatDict.items():
            self.logger.debug("filt={0}".format(filt))
            self.logger.debug("flat={0}".format(flat))
            if filt and filt in self.objects:
                applyFlat(flat,*self.objects[filt],save_inplace=True)
        return self

    def applyWCS(self,observatory = observatories.ROVOR):
        '''apply world coordinate systems to the images using data from
        the observatory information to set paramaters to astrometry.net'''
        self.ensure_objectList()
        for frames in self.objects.values():
            for frame in frames:
                header = pyfits.getheader(frame)
                ra = ':'.join(getRA(header))
                dec = ':'.join(getDec(header))
                astrometrySolve(frame,
                    guess=(ra,dec),
                    lowscale=observatory.lowscale, 
                    highscale=observatory.highscale,
                    outdir=path.join(self.folder,'WCS')
                )
        #astrometry.net names the new files with .new extension, rename them
        renamer.renameAll(path.join(self.folder,'WCS'),oldExt=".new")

def doSecondPass(path,flatDict):
    '''perform the second pass on images in the given folder'''
    improc = SecondPassProcessor(path)
    improc.applyFlats(flatDict)
    improc.applyWCS()

