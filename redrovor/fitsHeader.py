import os
import os.path
import re

import obsDB
import simbad

from collections import defaultdict
import pyfits

zeroRE = re.compile(r'([zZ]ero)|([Bb]ias)')
darkRE = re.compile(r'[dD]ark')
flatRE = re.compile(r'[Ff]lat')
objectRE = re.compile(r'([iI]mage)|([Ll]ight)|([oO]bject)')

fitsSuffixes = set(['.fits','.fts','.FIT','.FITS','.fit'])

def isFits(fname):
    '''Determine if the filename is right for a fits file or not'''
    return os.path.isfile(fname) and os.path.splitext(fname)[1] in fitsSuffixes

def fitsCheckMagic(fname):
    '''check the magic number to make sure it actually is a fits file'''
    with open(fname, 'rb') as fl:
        return fl.read(len('SIMPLE')) == 'SIMPLE'

def getFrameType(header):
    '''Given the header for a frame determine if it is a 
       zero, dark, flat, or image frame using the imagetyp header 
       and possibly the exposure time'''
    imtype = header['imagetyp']
    exptime = header['exptime']
    if zeroRE.search(imtype) or exptime == 0:
            return 'zero'
    elif darkRE.search(imtype):
            return 'dark'
    elif flatRE.search(imtype):
            return 'flat'
    elif objectRE.search(imtype):
            return 'object'
    else:
            return None

def getObjectName(header):
    '''get the name of the object in the frame'''
    if 'object' in header:
            return header['object'].replace('_',' ')
    elif 'title' in header:
            return header['title'].replace('_',' ')
    else:
        ra= header.get('objctra','0:0:0').replace(' ',':')
        dec = header.get('objctdec','0:0:0').replace(' ',':')
        try:
            name = obsDB.lookup_name(ra,dec)
            return str(name) #convert from unicode to string
        except obsDB.ObsDBError as e:
            #return 'unknown' #if there was a problem retrieving it is unknown
            #if we don't know the name create a name from RA and dec
            return makeRADecName(header)

def normalizedName(header):
    '''get a normalized name from simbad from the header, 
    
    this is just a convenience method which calls getObjectName and 
    then uses simbad to get the "main name" wich is the primary name 
    from simbad'''
    name = getObjectName(header)
    return simbad.getMainName(name)

def getFilter(header):
    if 'filter' in header:
        return header['filter']
    else:
        return 'unknown'

def getRA(header):
    '''get the Right Ascension and return a tuple containing the
    hour, minute and second'''
    if 'objctra' in header:
        return tuple(header['objctra'].split())
    elif 'ra' in header:
        return tuple(header['ra'].split())
    else:
        return None # ra isn't there

def getDec(header):
    ''' get the declination and return a tuple containing the degree,
    arcminute, and arcsecond, or None if no dec is there'''
    if 'objctdec' in header:
        return tuple(header['objctdec'].split())
    elif 'dec' in header:
        return tuple(header['dec'].split())
    else:
        return None

def makeRADecName(header):
    '''If we don't have the name of the object, build a name from the RA and 
    dec, but only use hours/degrees and minutes/arcminutes, so that we get a single
    name for each object. We may still get collisions, but it is better than
    just using unknown which would give us a lot more collisions'''
    ra = getRA(header)
    dec = getDec(header)
    if not ra or not dec:
        #either ra or dec was None so just return 'unknown'
        return 'unknown'
    return 'R{0}_{1}D{2}_{3}'.format(ra[0],ra[1],dec[0],dec[1])

def splitByHeader(imlist,keyword):
    '''split a list of filenames by a header keyword, throw out any non-fits 
    files.
    @returns a dict where the keys are the values of the supplied header and
    the values are lists of images which have that value in the header.
    
    if the keyword isn't in the header, then the empty string is used as 
    the value'''
    result = defaultdict(list)
    for im in iter(imlist):
        if isFits(im):
            #put each image into a list identified by the filter
            #if the filter keyword isn't supplied default to empty string
            result[pyfits.getheader(im).get(keyword,'')].append(im)
    return result
