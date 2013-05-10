#!/usr/bin/python


##
# program to print out the header of a FITS file
#

import sys

def printHeader(fitsfile):
	f = open(fitsfile,'r')
	card = ''
	while not card.startswith('END'):  # check to see if we have reached the end of the header
		card = f.read(80) #each "card" of the header is 80 characters
		if card.strip() != '':  # ignore empty lines
			print card


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: must supply a fits file to view"
		sys.exit(-1)
	printHeader(sys.argv[1])
