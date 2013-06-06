'''module to calculate paramaters for photometry, this
should only be used internally by the phot package'''

import pywcs
import numpy
import pyfits
from scipy.interpolate import UnivariateSpline as uniSpline
from scipy.stats import tstd

def getBox(image, center, size=100):
    ''' get a box centered at \p center with a size of \p size
    pixels.

    @param image the pyfits HDU object of the image to find the coordinates for
    @param center a coords.Coords object containing the WCS
        coordinates for the center of the box
    @param size the length of one side of the box in pixels
    '''
    #TODO figure out what to do about the order of coordinates (ra,dec) or (dec,ra) we don't
    #seem to have the right paramaters set

    mywcs = pywcs.WCS(image.header) #get WCS object
    ra,dec = center
    #we need to convert to decimal degrees before doing transformation
    r = float(ra.toDegrees())
    d = float(dec.toDegrees())
    x,y = mywcs.wcs_sky2pix([(r,d)],0)[0]  #perform conversion
    #get the bottom and left coordinates
    bottom = int(y-size/2)
    left = int(x-size/2)

    #numpy arrays are column major, so we give y vallues first
    return image.data[bottom:bottom+size,left:left+size]


def im_histogram(box,bins=1000):
    '''get the histogram of a numpy array, return (x,y) where
    x is the midpoints of the bins, and y is the number of pixels in each bin
    @param bins the number of bins to use'''

    y,bins = numpy.histogram(box,bins=bins)
    x = (bins[1:]+bins[:-1])/2  #compute the average of each consecutive pair of elements
    return (x,y)


class MultiplePeakError(Exception):
    '''more than one peak in the distribution'''
    pass

class NoPeakFoundError(Exception):
    '''no peak in distribution'''
    pass

def center_and_fwhm(x,y,bins=1000):
    '''calculate the full width half max of the function y(x),
    and get the center of the thing
    @returns (center, fwhm) where center is the x value of the center of the peak and fwhm is
    the full width half max of the peak
    
    we won't actually use this for now, but we will keep it case we want it later'''
    midx = numpy.argmax(y) #get index of maximum
    half_max = y[midx]/2 #get half the maximum
    center = x[midx] #get the value of the center

    s = uniSpline(x,y-half_max)  #create a spline of the data
    roots = s.roots()  #get roots of the spline, i.e. place of half-max
    if len(roots) > 2:
        #too many roots
        raise MultiplePeakError("There appears to be more than one peak")
    elif len(roots) < 2:
        raise NoPeakFoundError("There doesn't appear to be a proper peak")
    else:
        return (center, abs(roots[1]-roots[0]))

def background_data(imageName, center_coords, size=100):
    '''calculate the background value and standard deviations
    and return as a tuple (background, sigma)
    @param imageName the path to the image to get the data for
    @param center_coords the coordinates to center the sampling box around, probably the coordinates of the target object
    @param size the size of the sampling box in pixels
    @returns a modal value with bins of size 1 count and a trimmed standard deviation reject values more than twice the background value'''
    with pyfits.open(imageName) as im:
        box = getBox(im[0], center_coords,size)
    bins = numpy.arange(box.min(), box.max(),1) #use bins of size 1 ranging from the minimum to maximum values of the sample box
    x,y = im_histogram(box, bins=bins)
    #compute the location of the peak of the histogram
    midx = numpy.argmax(y)
    center = x[midx]
    sigma = tstd(box, [0,2*center]) #trim to twice the the peak value
    return (center, sigma)

