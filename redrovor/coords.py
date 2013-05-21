#!/usr/bin/python

import os
from collections import namedtuple


Coords = namedtuple('Coords',['ra','dec'])

def astrometrySolve(fname,**kwargs):
	'''use the framework from astrometry.net to apply 
	world coordinate systems to the file located at fname'''
	return os.system("/usr/local/astrometry/bin/solve-field {0} {1}".format(buildOptions(kwargs),fname))





def buildOptions(args):
    '''build a string for the options to the solve-field command, this should not be
    used directly, but as a helper for astrometrySolve'''
    if 'options' in args:
        optionStr = args['options']
    else:
        optionStr = ''
    if 'guess' in args:
        ra,dec = args['guess']
        radius = args.get('radius',2)
        optionStr += "--ra {0} --dec {1} --radius {2}".format(ra,dec,radius)
    if 'lowscale' in args:
        optionStr += "--scale-low " + args['lowscale']
    if 'highscale' in args:
        optionStr += "--scale-high " + args['highscale']
    return optionStr


