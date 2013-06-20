from collections import defaultdict
import os
from os import path
import pyfits
import json

import photometry
from photometry import phot
from utils import findFrames
from fitsHeader import normalizedName

import logging
logger = logging.getLogger("Rovor.thirdpass")

#go ahead and initialize the photometry package
photometry.init()

class ThirdPassProcessor:
    '''Class for taking care of all the processing
    for the third, pass. 
    
    For photometry this is kind of overkill,
    but it will make things easier when we add more to this phase
    '''

    def __init__(self, folder):
        '''initialize the class with the path of the folder that we are 
        going to process, this is most likley the WCS folder produced by
        the second pass.'''
        self.folder = folder
        self.objects = defaultdict(list)
    def buildObjectList(self):
        '''discover object frames in the folder, and what the targets are'''
        for im in findFrames(self.folder):
            header = pyfits.getheader(im)
            self.objects[normalizedName(header)].append(im)
        #now save the object lists
        with open(path.join(self.folder, 'objectLists.json'),'w') as f:
            json.dump(self.objects, f)
        return self
    def ensure_objectLists(self):
        '''ensure that self.objects is set'''
        if not self.objects:
            objectPath = path.join(self.folder, 'objectLists.json')
            #if we already made the file load it
            if path.isfile(objectPath):
                with open(objectPath,'r') as f:
                    self.objects = json.load(f)
            else:
                logger.info("Creating object lists")
                self.buildObjectList()
        return self
    def objectNames(self):
        '''Get the normalized names of the objects we
        are dealing with in this folder.'''
        self.ensure_objectLists()
        return list(self.objects.keys())
    def phot(self,obj_mapping,output_dir=None,**kwargs):
        '''
        Phot the frames in the folder

        obj_mapping must be a dict mapping the normalized name of objects
        to a tuple containing the coordinate file and optionally a 
        coords.Coords object  containing the coordinates of the target.
        output_dir is the directory to save the output folders in,
        it defaults to a subdirectory of self.folder named "photometry"
        and will be created if it does not already exist.

        all kwargs are passed through to the phot method
        '''
        logger.info("Photting folder: "+self.folder)
        self.ensure_objectLists()
        if output_dir is None:
            output_dir = path.join(self.folder,'photometry')
        if not path.isdir(output_dir):
            #only create directory if it does not already exist
            os.makedirs(output_dir)
        for objName, (coordfile,targetCoords) in obj_mapping.items():
            for im in self.objects[objName]:
                logger.info("Photting image: "+im)
                phot(im,output_dir,coordfile,targetCoords,**kwargs)
        return self
            
def doThirdPass(path, obj_mapping,output=None,**kwargs):
    '''perform the third pass, for now this just does the photometry, 
    although at some later point we may add other processing such as 
    combining data for the same object-filter combinations, not that this 
    uses the photometry package so changing the photometry package is 
    sufficient to change how photometry is done.
    also, additional options to control the phot process can be passed in 
    as kwargs
    '''
    proc = ThirdPassProcessor(path)
    return proc.phot(obj_mapping,output,**kwargs)


    
    
    
