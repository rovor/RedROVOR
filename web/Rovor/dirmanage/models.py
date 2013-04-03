from django.db import models

import os
import os.path as path

# Create your models here.

DATA_DIR = '/data'
PROCESSED_PATH = path.join(DATA_DIR,'Processed')
IMAGE_PATH = path.join(DATA_DIR, 'images')
CAL_PATH = path.join(DATA_DIR, 'Calibration')


class Filesystem(models.Model):
    fields = ( models.CharField('name','Name',maxlength=128),
        models.CharField('path','Path',maxlength=200),
    )

    def __repr__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/files/{0}/'.format(self.name)

    def isdir(self,path):
        import os
        
        p = os.path.realpath(os.path.join(self.path,path))
        if not p.startswith(self.path): raise ValueError(path)
        return os.path.isdir(p)

    def files(self, path=''):
        import os
        import mimetypes
        p = os.path.realpath(os.path.join(self.path,path))
        if not p.startswith(self.path): raise ValueError(path)
        l = os.listdir(p)
        if path: l.insert(0, '..')
            return [(f, os.path.isdir(os.path.join(p,f)), mimetypes.guess_type(f)[0] or 'application/octetstream') for f in l]

    def file(self, path):
        import os
        import mimetypes
        p = os.path.realpath(os.path.join(self.path,path))
        if p.startswith(self.path):
            (t,e) = mimetypes.guess_type(p)
            return (p, t or 'application/octetstream')
        else: raise ValueError(path)
    
    admin = models.Admin(
        fields = ( (None, {'fields': ('name','path')}) ),
        list_display = ('name','path'),
        search_fields = ('name', 'path'),
        ordering = ['name']
    )



