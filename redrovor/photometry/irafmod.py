import os
import tempfile
from decimal import Decimal

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
    iraf.daophot()
    iraf.obsutil()

    _initialized = True
    os.chdir(old_path) #restore original path
    return



def makeICommandFile(image,coord_file):
    '''create a temporary icommand file for getting the 
    fwhmpsf and skysigma from the daoedit command, it is kind
    of stupid that we need to do this, but IRAF just works that way
    and I really hate it'''
    #first get a temporary file
    f = tempfile.NamedTemporaryFile("r+",delete=False)
    f.close() # we don't need it yet and for some reason, keeping it open 
    #doesn't work
    #now get the coordinates for this image in logical system
    iraf.image()
    iraf.imcoord()
    oldclobber = iraf.show("clobber",Stdout=1)[0]
    iraf.set(clobber=yes)
    iraf.wcsctran(coord_file,f.name, image, "world","logical",verbose=no)
    iraf.set(clobber=oldclobber)
    f = open(f.name,"r+")
    #now read in the file
    lines = [ line.strip() + " logical a\n" for line in f.readlines()]
    f.seek(0) #rewind file
    f.writelines(lines)
    f.truncate()
    f.close()
    return f.name

def calcDAOparams(image,coord_file):
    '''calculate the fwhmpsf and skysigma for an image
    with the given coordinate file.'''
    #first get the command file
    icommands = makeICommandFile(image,coord_file)
    print icommands, "\n\n\n\n"
    output = iraf.daoedit(image,icommands=icommands,Stdout=1,Stderr='/dev/null')
    #initialize variables
    result = {'fwhm':0,'sky':0,'sigma':0}
    count = 0
    for line in output:
        if line.strip() and  not line.startswith('#'):
            print line
            vals = line.split()
            result['fwhm'] += Decimal(vals[4])
            result['sigma'] += Decimal(vals[3])
            count += 1
    result['fwhm'] /= count
    result['sky'] /= count
    result['sigma'] /= count
    return result
