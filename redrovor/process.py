import pyfits
import numpy

from datetime import datetime
from itertools import imap

class ImageList:
    '''A list of images on which to perform operations such as combining, subtracting, dividing etc'''
    
    def __init__(self, *args):
        '''create an image list from supplied filenames
            to create from a collection call like ImageList(*coll)
            '''
        self._list = [pyfits.open(fname) for fname in args] # initialize the list of images


    def averageAll(self, minmax=2):
        '''compute the average image of all images in the ImageList
        
        defaults to removing the two maximal and minimal values, changing
        the paramater minmax changes how many to remove on each end must be nonnegative
        there must also be at least 2*minmax + 1 frames in the ImageList
        
        returns a numpy array with the resulting data, up to suer to pack in FITS file'''

        n = len(self._list) - 2*minmax   # the number of frames involved in the average
        return self.sumAll(minmax) / n   # sum up the frames with minmax reject, and divide by the number of effective frames



    def sumAll(self, minmax=2):
        '''compute the sum of all images in the ImageList
        minmax is the number of values to leave off at the minimum and maximum ends
        set to 0 for no minmax reject
        
        Returns a numpy array with the resulting data, up to user to pack in a FITS file'''
        if minmax < 0:
            raise ValueError('minmax must be non-negative')
        if len(self._list) <= 2*minmax:
            raise ValueError('must have at least {0} items in ImageList with minmax={1}, only has {2}'.format(2*minmax+1,minmax,len(self._list)))
        #create a 3-d array with the first axis along the frames
        all = numpy.array(map(lambda im: im[0].data, self._list))
        all.sort(0) #sort along frame axis , so we can reject the min and maxes

        #now add them together to get the sum, leaving off the mins and maxes
        total = numpy.add.reduce(all[minmax:-minmax])  #reduce the add operation along the z-axis to get the sum of the images

        return total

    def avCombine(self,minmax=2):
        '''
        Combine all frames in the ImageList into a single frame by using an arithmetic mean with optional minmax rejection
        minmax defaults to 2, set to 0 for no minmax rejection, there must be at least 2*minmax+1 frames in the ImageList.
        
        At the moment this simply copies the header from the first frame, but we add more sophisticated manipulation of the header later.
        Returns a pyfits.PrimaryHDU
        '''
        result = pyfits.PrimaryHDU( self.averageAll(minmax), self._list[0][0].header)
        #NOTE: NAXIS, NAXIS1, NAXIS2, BITPIX, etc. should be updated to match the data portion
        result.header.update('NCOMBINE', len(self._list)) #store the number of images combined
        result.header.update('IRAF-TLM', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')) #store the time of last modification
        #TODO add code to modify header, at least mark the average time of observations, possibly the total exposure time
        # etc. 
        return result
            
    def closeAll(self):
        '''close all open files'''
        for f in self._list:
            if f:
                f.close()

    #guard code
    def __enter__(self):
        '''simply return self, to bind self to variable'''
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        '''close all open files'''
        self.closeAll()

    #iterators and accessors
    def hdulists(self):
        '''return an iterator over the HDULists in the list'''
        return iter(self._list)
    def hdus(self):
        '''return an iterator over the Primary HDUs'''
        return imap(lambda im: im[0], self._list)
    def headers(self):
        '''return an iterator over the headers of the images'''
        return imap(lambda im: im[0].header,self._list)
    def __iter__(self):
        '''alias for hdus, so default iterator is over hdus'''
        return self.hdus()
    def __len__(self):
        '''length of the list'''
        return len(self._list)

def makeZero(*fnames,**kwargs):
    '''
    Take the input frames,(which we assume to be zero or bias frames) as strings containging filnames
    and combine them into a master Zero. The exact behaviour depends on the following optional keyword arguments

    output -- if provided this is the path to write the resulting zero to, if absent makeZero will returning the resulting PrimaryHDU
    minmax -- if provided will set how many data points to remove from the top and bottom of the distribution, defaults to 2
    '''
    minmax = kwargs.get('minmax',2)  #get minmax with default of 2
    with ImageList(*fnames) as imList:
        Zero = imList.avCombine(minmax=minmax)
    Zero.header['imagetyp'] = 'zero' #make sure imagetyp is zero
    if 'output' in kwargs:
        Zero.writeto(kwargs['output'],clobber=True)

    

