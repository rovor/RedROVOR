'''classes for holding coordinate objects'''

from decimal import Decimal
from collections import namedtuple
import re

class RA_coord(object):
    '''A coordinate in RA'''

    ra_expr = re.compile(r'(\d{1,2})[: ](\d{1,2})[: ](\d{1,2}(\.\d+))?')
    def __init__(self,h,m,s):
        '''intialize with hours, minutes, and seconds
        note that the signs are ignored since RA is always positive '''
        if isinstance(s,float):
            s = "{0:.2}".format(s)
        self.h = abs(int(h))
        self.m = abs(int(m))
        self.s = abs(Decimal(s))
    def toHours(self):
        '''return the RA as a Decimal approximation'''
        return self.h+Decimal(self.m)/60 +Decimal(self.s)/3600
    def toDegrees(self):
        '''convert the RA to degrees and return the result as a Decimal'''
        return  self.toHours()*15
    def __str__(self):
        '''convert to a string of numbers seperated by colons'''
        return "{0:02}:{1:02}:{2:05.2f}".format(self.h,self.m,self.s)
    @classmethod
    def fromStr(cls,s):
        '''retrieve the RA from a string in the fromat hh:mm:ss.ss'''
        match = RA_coord.ra_expr.match(s)
        h,m,s = match.group(1,2,3)
        return cls(h,m,s)
    @classmethod
    def fromHours(cls,hrs):
        '''convert to RA_coord from decimal representation of RA in hours'''
        tmp = hrs
        h = int(tmp)
        tmp *= 60
        m = int(tmp % 60)
        tmp *= 60
        s = tmp % 60
        return cls(h,m,s)
    @classmethod
    def fromDegrees(cls, deg):
        '''create RA_coord from decimal representation in degrees'''
        if isinstance(deg,float):
            deg = "{0:.2}".format(deg)
        return cls.fromHours(Decimal(deg)/15)

    @property
    def hours(self):
        return self.h
    @property
    def minutes(self):
        return self.m
    @property
    def seconds(self):
        return self.s


        
class Dec_coord(object):
    '''A coordinate in declination'''

    dec_expr = re.compile(r'([+-]?\d{1,2})[: ](\d{1,2})[: ](\d{1,2}(\.\d+))?')
    def __init__(self,d,m,s):
        '''intialize with degrees, minutes, and seconds
        note that the signs are ignored for m and s, and the sign
        of the declination is determined by the sign of d'''
        if isinstance(s,float):
            s = "{0:.2}".format(s)
        self.d = int(d)
        self.m = abs(int(m))
        self.s = abs(Decimal(s))
    def toDegrees(self):
        '''return the dec as a Decimal approximation'''
        return self.d+Decimal(self.m)/60 +Decimal(self.s)/3600
    def __str__(self):
        '''convert to a string of numbers seperated by colons'''
        return "{0:+03}:{1:02}:{2:05.2f}".format(self.d,self.m,self.s)
    @classmethod
    def fromStr(cls,s):
        '''retrieve the dec from a string in the fromat hh:mm:ss.ss'''
        match = RA_coord.ra_expr.match(s)
        d,m,s = match.group(1,2,3)
        return cls(d,m,s)
    @classmethod
    def fromDegrees(cls,deg):
        '''convert to Dec_coord from decimal representation of dec in degrees'''
        tmp = deg
        h = int(tmp)
        tmp *= 60
        m = int(tmp % 60)
        tmp *= 60
        s = tmp % 60
        return cls(h,m,s)

    @property
    def degrees(self):
        return self.d
    @property
    def minutes(self):
        return self.m
    @property
    def seconds(self):
        return self.s

Coords = namedtuple('Coords',['ra','dec']) #type for tuple of ra and dec
