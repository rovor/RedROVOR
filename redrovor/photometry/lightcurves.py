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


#constant holding the list of fields to dump from phot files
FIELD_STR = "id,otime,mag,airmass,ifilter"

def photdump(files, output):
    '''dump photometric information in the given list of 
    photometry files into output

    output can be either a file-like object open for writing, or a string, 
    if it is a string it is the path to a file, which is then opened in 'w'
    mode. 

    photdump returns the (still open) file object when done.
    
    it dumpst the following fields in the given order:

    id
    otime (observation time)
    magnitude
    airmass
    ifilter
    '''
    irafmod.check_init("can't dump")
    if isinstance(output, str):
        output = open(output,'w')
    for pfile in files:
        iraf.pdump(pfile, FIELD_STR, iraf.yes, Stdout=output)
    return output

def photdump_all(globber,output):
    '''similar to photdump, except that instead 
    of a list of files, it takes a string, which is a
    glob expression for the files to use, 
    ex. *.nst.1'''
    irafmod.check_init("can't dump")
    if isinstance(output,str):
        output = open(output,'w')
    iraf.pdump(globber,FIELD_STR,iraf.yes,Stdout=output)
    return output


