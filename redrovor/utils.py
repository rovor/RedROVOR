import os
from datetime import datetime
from glob import glob
import sys

def ensure_dir(path):
    #first see if it is exists
    if os.path.exists(path):
        #now if it is a dir return successfully
        if os.path.isdir(path):
            return
        else:
            #a non-directory file, throw an error
            raise ValueError('Path to non-directory')
    else:
        #attempt to create the path
        os.makedirs(path)

def getTimeString(frmt='%Y-%m-%dT%H:%M:%S'):
    '''get a formatted timeString'''
    return datetime.now().strftime(frmt)
        
def writeListToFile(ll, ff=sys.stdout,delimeter='\n'):
	'''Write the supplied list to the given file, one element per line, with no other delimeters
ll -- The list of items to write
ff -- The file to write to (as in file object)
delimeter -- the delimeter between items in the list'''
	ff.write('\n'.join( str(item) for item in ll))
	return

def writeListToFileName(ll, fname, delimeter='\n'):
	'''write the list to the file given by fname (opens a file object for writing) '''
	with open(fname, 'w') as ff:
		writeListToFile(ll,ff,delimeter)
	return 

def findFrames(folder):
    '''find  all fits files in the folder (anything ending with .fits, .fit, .FIT, or .fts'''
    validExtensions = ['.fits','.fit','.FIT','.fts']
    frames=list()
    for ext in validExtensions:
        frames.extend( glob(folder+'/*'+ext) )
    return frames


def shell_quote(s):
    'quote string to be safe in shell'
    return "'" + s.replace("'",r"'\''") + "'"
