from django.db import models

from fields import RAField, DecField
from redrovor.coords import Coords

# Create your models here.


class Target(models.Model):
    '''model for target objects (i.e. astronomical objects we are observing)'''

    name = models.CharField(unique=True,max_length=100) #name we use for object
    simbadName = models.CharField(unique=True,max_length=100)  #the primary name for it in simbad
    ra = RAField()
    dec = DecField()

    def get_coords(self):
        return Coords(ra=self.ra,dec=self.dec)
    def set_coords(self, coords):
        '''set coordinates from a Coords object
        or tuple of ra and dec'''
        if not coords:
            self.ra = None
            self.dec = None
        else:
            self.ra, self.dec = coords

    coords = property(get_coords,set_coords)

    def __str__(self):
        return self.name


def getUploadPath(self, filename):
    '''compute the file path for an uploaded coordfile
    This assumes that the target field has been set'''
    return "coordfiles/{0:s}/{1:s}".format(self.target.name,filename)

class CoordFileModel(models.Model):
    '''model for coordinate files that have been uploaded'''
    target = models.ForeignKey(Target)  #the target the coordfile is for
    coordfile = models.FileField(upload_to=getUploadPath,null=True)
