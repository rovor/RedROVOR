from django.db import models
from django.forms import ModelForm

from fields import RAField, DecField
from coords import Coords

# Create your models here.




class Target(models.Model):
    '''model for target objects (i.e. astronomical objects we are observing)'''

    name = models.CharField(unique=True,max_length=100) #name we use for object
    simbadName = models.CharField(unique=True,max_length=100)  #the primary name for it in simbad
    ra = RAField()
    dec = DecField()

    @property
    def coords(self):
        return Coords(ra=ra,dec=dec)

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

#forms for the models

class TargetForm(ModelForm):
    class Meta:
        model = Target

class CoordFileModelForm(ModelForm):
    class Meta:
        model = CoordFileModel
