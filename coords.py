#!/usr/bin/python

import os

def astrometrySolve(fname):
	'''use the framework from astrometry.net to apply 
	world coordinate systems to the file located at fname'''
	os.system("/usr/local/astrometry/bin/solve-field {0}".format(fname))

