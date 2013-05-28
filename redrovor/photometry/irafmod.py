import os
import re

DEFAULT_IRAF_DIR = '/home/iraf'  #default directory to start iraf in

_initialized = False


class InitializationError(Exception):
    '''Error raised when a function of this module 
    is called before init() has been called'''
    def __init__(self,value=""):
        self.value = value
    def __str__(self):
        return 'Call attempted before init() was called: '+repr(self.value)

def init(iraf_dir=DEFAULT_IRAF_DIR):
    '''Initialize IRAF for use in photometry
    @param iraf_dir The home directory for iraf, i.e. where login.cl
    and uparm are located, slightly annoying that we need this, but not
    much we can do about it'''
    global _initialized 
    if _initialized:
        #already initialized no need to run again
        return
    old_path = os.getcwd()
    os.chdir(iraf_dir)
    global iraf
    global yes
    global no
    from pyraf import iraf
    yes = iraf.yes
    no = iraf.no
    #now load the packages we need
    iraf.noao()
    iraf.digiphot()
    iraf.apphot()
    iraf.obsutil()

    _initialized = True
    os.chdir(old_path) #restore original path
    return


def getAverageFWHM(image,coord_file):
    '''calculate the average Full Width Half Max for the objects in image
    at the coords specified in coord_file
    the coordinates in coord_file should be in the same world coordiantes
    as the WCS applied to the image'''
    if not _initialized:
        raise InitializationError()
    psfmeasure = iraf.psfmeasure
    #set up all paramaters
    psfmeasure.coords = "mark1"
    psfmeasure.wcs = "world"
    psfmeasure.display = no
    psfmeasure.size = "FWHM"
    psfmeasure.imagecur = coord_file
    psfmeasure.graphcur = '/dev/null' #file that is empty by definition
    res = psfmeasure(image,Stdout=1)[-1]  #get last line of output
    match = getAverageFWHM.numMatch.search(res)
    return float(match.group(1))

getAverageFWHM.numMatch = re.compile(r'(\d+(\.\d+)?)')





