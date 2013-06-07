#!/usr/bin/python

'''A Module to take care of renaming fits files to a more friendly extension (i.e. fit instead of FIT).'''

import os
import fitsHeader


def renameFITS(origFile,newExt=".fit"):
    '''Rename a single fits file to have the extension provided (defaults to .fit)
    origFile is a string with the correct path to the file to rename (absolute or relative to working directory)
    return true if the rename was successful, false otherwise'''
    if os.path.isfile(origFile):
        newName = os.path.splitext(origFile)[0] + newExt
        try:
            os.rename(origFile,newName)
            return True
        except OSError:
            return False

    else:
        return False


def renameAll(path,newExt=".fit", oldExt=".FIT"):
    '''Rename all FITS files with extension oldExt to extension newExt (defaults
    to .fit) which are in directory path. If path is empty or not a directory
    renameAll will silently return without doing anything.
    '''
    if not os.path.isdir(path):
        return
    for f in os.listdir(path):
        if f.endswith(oldExt):
            renameFITS(os.path.join(path,f),newExt)




