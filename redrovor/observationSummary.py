#!/usr/bin/python
from collections import defaultdict
import json

import os
from os import path
import sys
import fitsHeader

import pyfits


class observationSummary :
    '''basically a wrapper around a dictionary mapping the 
    name of the target to a dictionary mapping the filter type to the number
    of images in that filter'''
    def __init__(self):
        #initialize the rather complicated underlying data structure
        #we use defaultdict to make it easier to increment stuff
        self._data = defaultdict(lambda: defaultdict(lambda:0))
        return
    def addObservation(self, targetName, ifilter):
        '''record a new observation of targetName, in filter ifilter
        i.e. increment the count of that name and filter, return the new count'''
        self._data[targetName][ifilter] += 1
        return self._data[targetName][ifilter]
    def parseHeader(self, header):
        '''parse a FITS header, and if the image is an
        object frame add the information to the summary
        return true if an object, false otherwise'''
        if fitsHeader.getFrameType(header) == 'object':
            targetName = fitsHeader.getObjectName(header)
            filterName = fitsHeader.getFilter(header)
            self.addObservation(targetName, filterName)
            return True
        else:
            return False
    def __getitem__(self, targetName):
        '''return a dictionary mapping filter type to number in that filter'''
        return self._data[targetName]
    def __len__(self):
        return len(_data)
    def __iter__(self):
        '''iterate over targetNames'''
        return iter(self._data)
    def iteritems(self):
        '''iterate over all targetName, filter combinations'''
        for (targetName, ifilters) in self._data.iteritems():
            for (ifilter, num) in ifilters_.iteritems():
                yield( targetName, ifilters, num)
    def getJson(self):
        '''get the json string for the dictionary'''
        return json.dumps(self._data)
    def __str__(self):
        '''the string representation will be:
        targetName:
                filterName  num
        repeated for each targetname'''
        result = ''
        for (targetName, ifilters) in self._data.iteritems():
            result += '{0}:\n'.format(targetName)
            for (ifilter, num) in ifilters.iteritems():
                result += '\t{0} {1}\n'.format(ifilter,num)
        return result


def buildSummary(folder="."):
    '''Look through all FITS files in the folder given
    and return an observationSummary containing summary information
    about the object frames (i.e. the number of images in each filter for 
    each target)
    defaults to current directory'''
    summary = observationSummary()
    for f in os.listdir(folder):
        fullName = os.path.join(folder, f)
        if fitsHeader.isFits(fullName):
            header = pyfits.getheader(fullName)
            summary.parseHeader(header)
    return summary

def main(folder=".", outputBase="obsSummary",recursive=False):
    '''main function'''
    #properly set the output base to match the folder we are running on
    fullBase = os.path.join(folder,outputBase)

    summary = buildSummary(folder)
    with open(fullBase,'w') as txtFile:
        txtFile.write(str(summary))
    with open(fullBase + ".json", 'w') as jsonFile:
        jsonFile.write(summary.getJson())
    if recursive:
        for file in os.listdir(folder):
            fname = os.path.join(folder,file)
            if os.path.isdir(fname):
                main(fname, outputBase, True)
    

if __name__ == '__main__':
    #main function (sort of)

    import getopt

    
    try:
        options,args = getopt.gnu_getopt(sys.argv[1:],"r")
    except getopt.GetoptError, err:
        print str(err)
        print "Usage: observationSummary.py [-r] [folder [outputBase]]"
        sys.exit(2)
    
    recursive = False
    
    for o, a in options:
        if o == "-r":
            recursive = True
        else:
            assert False, "unhandled option"

    if len(args) > 0:
        folder = args[0]
    else:
        folder = "."

    if len(args) > 1:
        outputBase = args[1]
    else:
        outputBase = "obsSummary"

    main(folder, outputBase,recursive)
    


    
