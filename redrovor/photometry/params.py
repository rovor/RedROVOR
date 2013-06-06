'''this module takes care of setting up paramaters
for iraf tasks'''

from calc_params import getAverageFWHM, background_data 



class Params(dict):
    '''class to take care of holding paramaters, this is more abstract
    and is intended as a superclass for classes that can actually set the
    IRAF paramaters, it is sort of a wrapper around a dictionary'''
    def __init__(self,**kwargs):
        #start with default options
        defaults = {
            'aperture_ratio':1.2,
            'annulus_ratio':4,
            'dannulus_ratio':3,
            'zmag': 25,
            #header keywords
            'obstime':'date-obs',
            'exposure':'exptime',
            'airmass':'airmass',
            'filter':'filter',
            'datamax': 50000, #point where CCD saturates
        }
        defaults.update(kwargs)
        super(Params,self).__init__(defaults)

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
    def annulus(self):
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
    def __init__(self,**kwargs):
        super(DAO_params,self).__init__(**kwargs)
        #default paramaters for datapars

    def applyParams(self):
        '''apply paramaters for daophot'''
        #photpars
        iraf.photpars.aperture = self.aperture
        iraf.photpars.zmag = self['zmag']
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
        #make sure we are using world coordinate system
        iraf.daophot.wcsin="world"
        iraf.daophot.wcsout="world"


def getDAOParams(imageName, coord_file, target_coords=None, size=100, **kwargs):
    '''calculate the paramaters for performing daophot for an image
    using the coordinate file and possibly the coordinate of the target,
    if target_coords is None or not supplied, we assume that the target is the
    first set of coordinates in the coordinate file.

    The target coordinates are used to estimate the background and background sigma.
    size is the size of the sampling box for getting sigma and background'''
    if target_coords is None:
        target_coords = parse_first_coords(coord_file)
    params = DAO_params(**kwargs)
    params['fwhm'] = getAverageFWHM(imageName, coord_file)
    params['background'], params['sigma'] = background_data(imageName, target_coords,size)
    return params
