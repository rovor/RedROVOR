'''this module takes care of setting up paramaters
for iraf tasks'''

from irafmod import getAverageFWHM



class Params(dict):
    '''class to take care of holding paramaters, this is more abstract
    and is intended as a superclass for classes that can actually set the
    IRAF paramaters, it is sort of a wrapper around a dictionary'''
    def __init__(self,**kwargs):
        #start with default options
        defaults = {
            'aperture_ratio':1.5,
            'annulus_ratio':3.2,
            'dannulus':10,
            'zmag': 25,
            #header keywords
            'obstime':'date-obs',
            'exposure':'exptime',
            'airmass':'airmass',
            'filter':'filter'
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

    def calculate_fwhm(self,image,coord_file):
        '''calculate the average full width half max and
        set the fwhm property using getAverageFWHM'''
        self['fwhm'] = getAverageFWHM(image,coord_file)
        return self['fwhm']




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
        iraf.datapars.fwhmpsf = self['fwhmpsf']
        iraf.datapars.sigma = self.get('sigma')
        iraf.datapars.obstime = self['obstime']
        iraf.datapars.exposure = self['exposure']
        iraf.datapars.airmass = self['airmass']
        iraf.datapars.filter = self['filter']
        #fitskypars
        iraf.fitskypars.annulus = self.annulus
        iraf.fitskypars.dannulus = self['dannulus']

        #make sure we are using world coordinate system
        iraf.daophot.wcsin="world"
        iraf.daophot.wcsout="world"


