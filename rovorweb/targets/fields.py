from django.db import models
from django.core.exceptions import ValidationError

from coords import RA_coord, Dec_coord

import forms

class RAField(models.Field):
    description = "The Right Ascension of an object or image"

    __metaclass__  = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        #11 max possible 2 colons, 2 digits for h,m,s a period and two decimal
        #points for s
        kwargs['max_length'] = 11
        super(RAField,self).__init__(*args,**kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self,value):
        '''get python value from serialized place'''
        if isinstance(value,str) or isinstance(value,unicode):
            try:
                return RA_coord.fromStr(value)
            except:
                raise ValidationError("Invalid input for RA: "+value)
        elif isinstance(value, RA_coord) or value is None:
            return value
        else:
            raise TypeError("unable to convert {0} of type {1} to RA_coord",value,type(value).__name__)
    def get_prep_value(self,value):
        '''prepare value for serialization'''
        return str(value)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            #we only implement exact and in for now
            raise TypeError('Lookup type {0} not supported.'.format(lookup_type))

    def value_to_string(self,obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
    
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.RAField}
        defaults.update(kwargs)
        return super(RAField, self).formfield(**defaults)
        



class DecField(models.Field):
    description = "The Declination of an object or image"

    __metaclass__  = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        #11 max possible 2 colons, 2 digits for h,m,s a period and two decimal
        #points for s
        kwargs['max_length'] = 12
        super(DecField,self).__init__(*args,**kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self,value):
        '''get python value from serialized place'''
        if isinstance(value,str) or isinstance(value,unicode):
            try:
                return Dec_coord.fromStr(value)
            except:
                raise ValidationError("Invalid input for Declination:"+str(value))
        elif isinstance(value, Dec_coord) or value is None:
            return value
        else:
            raise TypeError("unable to convert to Dec_coord")
    def get_prep_value(self,value):
        '''prepare value for serialization'''
        return str(value)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            #we only implement exact and in for now
            raise TypeError('Lookup type {0} not supported.'.fomrat(lookup_type))

    def value_to_string(self,obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.DecField}
        defaults.update(kwargs)
        return super(DecField, self).formfield(**defaults)



