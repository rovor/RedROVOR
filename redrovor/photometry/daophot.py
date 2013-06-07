'''module for actually performing daophot'''

import irafmod
from params import getDAOParams

def phot(imageName, coordFile, target_coords=None,sample_size=100,params=None,**kwargs):
    '''perform daophot on imageName with the supplied
    coordinate file, and optionally the target coordinates, which
    defaults to the first coordinates in coordFile

    sample_size is the size of the sample box used for background measurement
    kwargs are additional args to pass to constructor for params (or update params)'''

    #first ensure that irafmod has been initialized
    if not irafmod._initialized:
        raise InitializationError("unable to phot")
    daophot = irafmod.iraf.daophot

    #first get the paramaters we need
    if not params:
        params = getDAOParams(imageName, coordFile, target_coords, size=sample_size)
    params.update(kwargs)
    params.applyParams()

    daophot.phot(imageName,coordFile,"default")
    daophot.pstselect(imageName,"default","default")
    #params: imagename photfile pstfile psfimage opstfile groupfile
    daophot.psf(imageName,"default","default","default","default","default",
        interactive=irafmod.no)
    #TODO should we be more sophisticated and do multiple runs of psf
    #along with using nstar and substar to try and get best fit?

    #use nstar for now, but we will make it a seperate function
    #so it is easy to switch out with peak or allstar
    #if we desire later
    do_nstar(imageName)


def do_nstar(imageName):
    '''perform nstar stuff, should not be called by user code
    only a helper for phot'''
    daophot = irafmod.iraf.daophot
    daophot.group(imageName,"default","default","default")
    #we will assume that we don't have any big groups for now, 
    #so we don't have to use grpselect
    daophot.nstar(imageName,"default","default","default","default")


def do_allstar(imageName):
    '''perform allstar stuuf, should only be called by phot'''
    irafmod.iraf.daophot.allstar(imageName,"default","default","default","default","default")
    






