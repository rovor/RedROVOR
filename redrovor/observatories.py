
from decimal import Decimal

class observatory:
    def __init__(self,width=Decimal(1),height=Decimal(1),lowscale=Decimal('0.1'),highscale=Decimal('2'),**kwargs):
        self.__dict__['_dict'] = kwargs
        self._dict['units'] = 'degrees' #default units are degrees
        self._dict['width'] = Decimal(width)
        self._dict['height'] = Decimal(height)
        self._dict['lowscale'] = Decimal(lowscale)  #value for low scale when using astrometry.net
        self._dict['highscale'] = Decimal(highscale) #value for high scale when using astrometry.net
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
ROVOR = observatory(width=Decimal(23)/60,height=Decimal(23)/60,lowscale='0.3',highscale='0.4')

