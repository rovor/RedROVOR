'''this module takes care of setting up paramaters
for iraf tasks'''

from calc_params import getAverageFWHM, background_data 

from redrovor.coords import Coords, RA_coord, Dec_coord

import irafmod



class Params(dict):
    '''class to take care of holding paramaters, this is more abstract
    and is intended as a superclass for classes that can actually set the
    IRAF paramaters, it is sort of a wrapper around a dictionary'''
    def __init__(self,observ,**kwargs):
        #start with default options
        #TODO some of these are dependent on the system
        # we should make a way to abstract those part out into 
        # a seperate object for system-dependent permanent settings
        defaults = {
            'aperture_ratio':1.2,
            'annulus_ratio':4,
            'dannulus_ratio':3,
            'zmag': 25,
            'datamax': observ.datamax, #point where CCD saturates
            #header keywords
            'obsdate':observ.date_key,
            'obstime':observ.time_key,
            'exposure':observ.exp_key,
            'airmass':observ.air_key,
            'filter':observ.filt_key,
            'epoch': observ.epoch_key,
            'ra_key': observ.ra_key,
            'dec_key':observ.dec_key,
            'observat':observ.name, #this needs to be set up for the right telescope
        }
        super(Params,self).__init__(defaults)
        self.update(kwargs)

    def __call__(self,*args,**kwargs):
        '''calling the method simply forwards the call to
        applyParams with the supplied arguments, it is expected
        that the subclass will implement applyParams, it is not
        implemented in this class'''
        self.applyParams(*args,**kwargs)

    @property
    def aperture(self):
        '''return the aperture in scale units'''
        return self['aperture_ratio']*self['fwhm']
    @property
    def annulus(self):
        '''return a tuple of the inner and outer annuli in scale units'''
        return self['annulus_ratio']*self['fwhm']
    @property
    def dannulus(self):
        '''return a tuple of the inner and outer annuli in scale units'''
        return self['dannulus_ratio']*self['fwhm']

    @property
    def datamax(self):
        '''return the maximum good data value'''
        return self.get('datamax','INDEF')
    @property
    def datamin(self):
        '''return the minimum good data value'''
        if 'datamin' in self:
            return self['datamin']
        elif 'background' in self and 'sigma' in self:
            #minimum good data is 6 sigma below background
            return self['background'] - 6.0*self['sigma']
        else:
            return 'INDEF'
    @property
    def cbox(self):
        '''return size for center box, if not explicetly set use
        maximum of 5 and 2*fwhm'''
        return self.get('cbox',max(5.0, 2.0*self['fwhm']))


class DAO_params(Params):
    '''class to take care of setting up paramaters for dao photting'''
    def __init__(self,observ,**kwargs):
        super(DAO_params,self).__init__(observ,fitfunction='gauss',
            readnoise=observ.readnoise,gain=observer.gain)
        self.update(kwargs)

    def applyParams(self):
        '''apply paramaters for daophot'''
        if not irafmod._initialized:
            raise irafmod.InitializationError("DAO_params.applyParams")
        iraf = irafmod.iraf

        #photpars
        iraf.photpars.aperture = self.aperture
        iraf.photpars.zmag = self['zmag']
        #set world coordinates as input for phot
        iraf.phot.wcsin="world"
        #datapars
        iraf.datapars.fwhmpsf = self['fwhm']
        iraf.datapars.sigma = self.get('sigma',0)
        iraf.datapars.datamax = self.datamax
        iraf.datapars.datamin = self.datamin
        iraf.datapars.obstime = self['obstime']
        iraf.datapars.exposure = self['exposure']
        iraf.datapars.airmass = self['airmass']
        iraf.datapars.filter = self['filter']
        #centerpars
        iraf.centerpars.cbox = self.cbox
        iraf.centerpars.calgorithm = self.get('calgorithm','centroid')
        #fitskypars
        iraf.fitskypars.annulus = self.annulus
        iraf.fitskypars.dannulus = self.dannulus
        iraf.fitskypars.salgorithm = self.get('salgorithm','mode')
        #daopars
        iraf.daopars.psfrad = 4.0*self['fwhm']+1.0
        iraf.daopars.fitrad = self.aperture
        #psfpars
        iraf.psf.function = self['fitfunction']
        #make sure we are using default logical coordinate system
        #for everything except the phot command
        iraf.daophot.wcsin="logical"
        iraf.daophot.wcsout="logical"
        iraf.daophot.verify=iraf.no
        # setjd paramaters
        iraf.setjd.date = self['obsdate']
        iraf.setjd.time = self['obstime']
        iraf.setjd.exposur = self['exposure']
        iraf.setjd.epoch = self['epoch']
        iraf.setjd.ra = self['ra_key']
        iraf.setjd.dec = self['dec_key']



def getDAOParams(observ,imageName, coord_file, target_coords=None, size=100, **kwargs):
    '''calculate the paramaters for performing daophot for an image
    using the coordinate file and possibly the coordinate of the target,
    if target_coords is None or not supplied, we assume that the target is the
    first set of coordinates in the coordinate file.

    The target coordinates are used to estimate the background and background sigma.
    size is the size of the sampling box for getting sigma and background'''
    if target_coords is None:
        target_coords = parse_first_coords(coord_file)
    params = DAO_params(observ,**kwargs)
    params['fwhm'] = getAverageFWHM(imageName, coord_file)
    params['background'], params['sigma'] = background_data(imageName, target_coords,size)
    return params

def parse_first_coords(coord_file):
    '''parse the coordinates of the first object
    in the coordinate file and return a Coords object'''
    with open(coord_file) as cf:
        line = cf.readline()
        while line and (line.isspace() or line.startswith('#')):
            #skip over blank lines and comments
            line = cf.readline()
    if not line:
        raise Exception("Unable to parse coordinates") #TODO use better exception type
    rastr, decstr = line.split()[0:2] #assume seperationg by whitespace and no internal whitespace
    ra = RA_coord.fromStr(rastr)
    dec = Dec_coord.fromStr(decstr)
    return Coords(ra,dec)

