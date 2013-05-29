from django.db import models

from fields import RAField, DecField
from coords import Coords

# Create your models here.




class Target(models.Model):
    '''model for target objects (i.e. astronomical objects we are observing)'''

    name = models.CharField(max_length=100) #name we use for object
    simbadName = models.CharField(max_length=100)  #the primary name for it in simbad
    ra = RAField()
    dec = DecField()

    @property
    def coords(self):
        return Coords(ra=ra,dec=dec)
