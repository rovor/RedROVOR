'''module to perform various operations to manipulate
the output from photting specifically related to producing 
lightcurves'''

import irafmod
import os

def sortphotfiles(folder, suffix=".nst.1"):
    '''sort all of the phot files in \p folder
    by id. They must end in \p suffix, which defaults to
    .nst.1'''
    irafmod.check_init("can't sort")
    irafmod.iraf.psort(os.path.join(folder,"*"+suffix),'id')
    return

