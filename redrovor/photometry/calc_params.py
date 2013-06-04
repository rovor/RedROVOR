'''module to calculate paramaters for photometry, this
should only be used internally by the phot package'''

import pywcs

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
    dec = float(dec.toDegrees())
    x,y = mywcs.wcs_sky2pix([(r,d)],0)[0]  #perform conversion
    #get the top and left coordinates
    top = int(y-size/2)
    left = int(x-size/2)

    return image.data[left:left+size,top:top+size]



