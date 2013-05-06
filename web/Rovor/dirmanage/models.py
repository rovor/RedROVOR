from django.db import models

import os
import os.path as path
import re

# Create your models here.

class Filesystem(models.Model):
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=200)

    splitRegExp = re.compile(r'/?(?P<name>.*?)/(?P<path>.*)')

    def __repr__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/files/{0}/'.format(self.name)
    def get_choose_path(self):
        return '/files/chooseFrame/{0}/'.format(self.name)
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
        if path: 
            l.insert(0, '..')
        return [(f, os.path.isdir(os.path.join(p,f)), mimetypes.guess_type(f)[0] or 'application/octetstream') for f in l]

    def file(self, path):
        import os
        import mimetypes
        p = os.path.realpath(os.path.join(self.path,path))
        if p.startswith(self.path):
            (t,e) = mimetypes.guess_type(p)
            return (p, t or 'application/octetstream')
        else: raise ValueError(path)


    @classmethod
    def getTruePath(cls, vpath):
        '''
        get the true path from the virtual path, which consists of the name
        of subsystem append to the path in the subsystem

        if the vpath begins with a directory other than one of the 
        registered names for a filesystme, then this will throw a DoesNotExist
        error. If the path is above the top of the assigned filesystem, throw
        a ValueError, and if the path isn't valid throw an IOError
        '''
        #start by splitting the name from the rest of path
        match = cls.splitRegExp.match(vpath)
        if not match:
            raise ValueError(vpath) #path isn't formatted correctly
        name = match.group('name')
        path = match.group('path')
        #now try to get the object for it
        fs = cls.objects.get(name=name) #will through DoesNotExist if fail
        p = os.path.realpath(os.path.join(fs.path,path))
        if p.startswith(fs.path):
            return p
        else:
            raise ValueError(path)
        
