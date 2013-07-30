import os
import tempfile
from decimal import Decimal
from redrovor.utils import workingDirectory

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
    global iraf
    global yes
    global no
    with workingDirectory(iraf_dir):
        from pyraf import iraf
        yes = iraf.yes
        no = iraf.no
        #now load the packages we need
        iraf.noao()
        iraf.digiphot()
        iraf.daophot()
        iraf.obsutil()

        _initialized = True
        return

def check_init(error_msg="Not initialized"):
    '''check that the irafmod module has been initialized'''
    if not _initialized:
        raise InitializationError(error_msg)

