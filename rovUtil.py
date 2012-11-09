
import sys

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
	 

