
from decimal import Decimal

class Observatory:
    '''class to hold constants for a specific observatory,
    this should be set for any observatory you use.
    
    The name should be the name of the observatory and should
    match the name of the observatory in the IRAF observatory
    database. This is necessary for the HJD to be set when photting.
    
    For accurate photometry the readnoise and gain of the detector should
    be set to good values for the system.'''
    def __init__(self,
        name, #name of the observatory, should match IRAF observatory database
        width=Decimal(1),
        height=Decimal(1),
        lowscale=Decimal('0.1'),
        highscale=Decimal('2'),
        ra_key = 'objctra',
        dec_key = 'objctdec',
        exp_key = 'exptime',
        date_key = 'date-obs',
        time_key = 'date-obs',
        epoch_key = 'equinox',
        air_key = 'airmass',
        filt_key = 'filter',
        datamax = 50000,
        #these should be properly set for accurate photometry
        readnoise = 0, 
        gain = 1,
        **kwargs):

        self.__dict__['_dict'] = kwargs
        self._dict['name'] = name
        self._dict['units'] = 'degrees' #default units are degrees
        self._dict['width'] = Decimal(width)
        self._dict['height'] = Decimal(height)
        self._dict['lowscale'] = Decimal(lowscale)  #value for low scale when using astrometry.net
        self._dict['highscale'] = Decimal(highscale) #value for high scale when using astrometry.net
        self._dict['ra_key'] = ra_key
        self._dict['dec_key'] = dec_key
        self._dict['exp_key'] = exp_key
        self._dict['date_key'] = date_key
        self._dict['time_key'] = time_key
        self._dict['epoch_key'] = epoch_key
        self._dict['air_key'] = air_key
        self._dict['filt_key'] = filt_key
        self._dict['datamax'] = datamax
        self._dict['readnoise'] = readnoise
        self._dict['gain'] = gain
    def __getitem__(self,key):
        return self._dict[key]
    def __setitem__(self,key,value):
        self._dict[key] = value
    def __getattr__(self,name):
        if name == '_dict':
            return self.__dict__[name]
        else:
            return self._dict[name]
    def __setattr__(self,name,value):
        self._dict[name] = value

        




#constants for the ROVOR observatory
ROVOR = Observatory('rovor',width=Decimal(23)/60,height=Decimal(23)/60,lowscale='0.3',highscale='0.4')

