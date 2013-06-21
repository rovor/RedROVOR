'''module for actually performing daophot'''

import irafmod
from params import getDAOParams
from redrovor.utils import workingDirectory
from redrovor.observatories import ROVOR


def phot(imageName, output_dir,coordFile, target_coords=None,
    sample_size=100,params=None,observat=ROVOR,**kwargs):
    '''perform daophot on imageName with the supplied
    coordinate file, and optionally the target coordinates, which
    defaults to the first coordinates in coordFile

    sample_size is the size of the sample box used for background measurement
    kwargs are additional args to pass to constructor for params (or update params)'''

    #first ensure that irafmod has been initialized
    irafmod.check_init("unable to phot")
    daophot = irafmod.iraf.daophot

    #first get the paramaters we need
    if not params:
        params = getDAOParams(observat,imageName, coordFile, 
            target_coords, size=sample_size)
    params.update(kwargs)
    params.applyParams()

    with workingDirectory(output_dir):
        #temporarily change working directory

        irafmod.iraf.setjd(imageName)
        daophot.phot(imageName,coordFile,"default")
        #params:  image, photfile, pstfile, maxnpsf
        daophot.pstselect(imageName,"default","default",25)
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
    






