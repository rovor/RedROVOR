#!/usr/bin/python

import os
from subprocess import Popen
from collections import namedtuple


SOLVE_PATH = "/usr/local/astrometry/bin/solve-field"

Coords = namedtuple('Coords',['ra','dec'])

def astrometrySolve(*fnames,**kwargs):
    '''use the framework from astrometry.net to apply 
    world coordinate systems to the files located at fnames'''
    with open(os.devnull, 'w') as dnull:
        proc = Popen(buildArgList(fnames,kwargs),stdout=dnull,stderr=dnull )
    return proc.wait() #wait until it completes, we may want to do some threading so that we can do more than one at at a time, but not all of them at once 
    #which would fill up memory really fast

        





def buildArgList(fnames,args):
    '''build a string for the options to the solve-field command, this should not be
    used directly, but as a helper for astrometrySolve'''
    result = [SOLVE_PATH]
    if 'options' in args:
        result.extend(args['options'])
    if 'guess' in args:
        ra,dec = args['guess']
        radius = args.get('radius',1)
        result.extend(['--ra',str(ra),'--dec',str(dec),'--radius',str(radius)])
    if 'lowscale' in args:
        result.extend(['--scale-low',str(args['lowscale'])])
    if 'highscale' in args:
        result.extend(['--scale-high',str(args['highscale'])])
    if 'outdir' in args:
        result.extend(['--dir',args['outdir']])
    if args.get('isfits',True):
        result.append('--fits-image')
    result.extend(['--no-plots','--no-fits2fits']) #disable making plots and sanitizing fits files
    result.extend(fnames)
    print result
    return result


