'''module to perform various operations to manipulate
the output from photting specifically related to producing 
lightcurves'''

import irafmod
import os

from cStringIO import StringIO

def sortphotfiles(folder, suffix=".nst.1"):
    '''sort all of the phot files in \p folder
    by id. They must end in \p suffix, which defaults to
    .nst.1'''
    irafmod.check_init("can't sort")
    irafmod.iraf.psort(os.path.join(folder,"*"+suffix),'id')
    return


#constant holding the list of fields to dump from phot files
FIELD_STR = "id,ifilter,otime,mag,airmass"

def photdump(files, output):
    '''dump photometric information in the given list of 
    photometry files into output

    output can be either a file-like object open for writing, or a string, 
    if it is a string it is the path to a file, which is then opened in 'w'
    mode. 

    photdump returns the (still open) file object when done.
    
    it dumpst the following fields in the given order:

    id
    ifilter
    otime (observation time)
    magnitude
    airmass
    '''
    irafmod.check_init("can't dump")
    iraf = irafmod.iraf
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
    iraf = irafmod.iraf
    if isinstance(output,str):
        output = open(output,'w')
    iraf.pdump(globber,FIELD_STR,iraf.yes,Stdout=output)
    return output

def splitdump(dumpfile,prefix):
    '''split a phot dump into seperate files for each id and filter 
    combination.

    dumpfile is a file like object open for reading in text mode,
    unfortunately it would be rather difficult to also support opening
    the file for you. Sorry'''
    fdict = {}
    try:
        for line in dumpfile:
            starid, filt, *rest = line.split()
            if (starid, filt) not in fdict:
                fdict[(starid,filt)] = open(prefix+"_"+filt+"_"+starid+".lc",'w')
            fdict[(starid,filt)].write('  '.join(rest)+"\n")
    finally:
        for f in fdict.values():
            #close all the open files
            f.close()
def makeLightCurves(photFiles, prefix):
    '''Create light curves for an object.

    photFiles is a list of photometry files, such as nst files
    which will be dumped to create the light curves.

    prefix is the prefix to save the light curves to. This should be the
    full path to the folder to save it in, and probably the name of the target or field.
    The prefix will be appended with the filter and the object id and the suffix .lc.'''
    #how hard would it be to parallelize this and pipe the result of photdump to the input of
    # splitdump
    buffer = StringIO()
    photdump(photFiles, buffer)
    buffer.reset() #reset to beginning of 'file' for reading
    splitdump(buffer, prefix)
    buffer.close()
    return True
    



