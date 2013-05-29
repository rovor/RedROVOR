from django import forms
from coords import RA_coord, Dec_coord
from decimal import Decimal



class RAField(forms.MultiValueField):
    '''Form field for inputting RA'''
    def __init__(self, **kwargs):
        fields = [
            forms.IntegerField(min_value=0,max_value=23), 
            forms.IntegerField(min_value=0,max_value=59),
            forms.DecimalField(min_value=Decimal(0),max_value=Decimal('59.99'))
        ]
        super(RAField,self).__init__(fields=fields, widget = RAWidget, **kwargs)
    def compress(self, data_list):
        '''compress field into RA_coord'''
        return RA_coord(*data_list)


class RAWidget(forms.MultiWidget):
    '''Widget for creating RA input'''

    def __init__(self, attrs=None):
        '''initalize RAWidget '''
        nattrs = {'maxlength':2, 'size':2}
        sattrs = {'maxlength':5, 'size':5}
        widgets  = [
            forms.widgets.TextInput(attrs=nattrs), 
            forms.widgets.TextInput(attrs=nattrs), 
            forms.widgets.TextInput(attrs=sattrs)
        ]
        super(RAWidget,self).__init__(widgets=widgets,attrs=attrs)

    def decompress(self, value):
        if value:
            return [value.hours, value.minutes, value.seconds]
        return [None, None, None]





class DecField(forms.MultiValueField):
    '''Form field for inputting Dec'''
    def __init__(self, **kwargs):
        fields = [
            forms.IntegerField(min_value=-90,max_value=90), 
            forms.IntegerField(min_value=0,max_value=59),
            forms.DecimalField(min_value=Decimal(0),max_value=Decimal('59.99'))
        ]
        super(DecField,self).__init__(fields=fields, widget = DecWidget, **kwargs)
    def compress(self, data_list):
        '''compress field into RA_coord'''
        return Dec_coord(*data_list)




class DecWidget(forms.MultiWidget):
    '''Widget for creating Dec input'''

    def __init__(self, attrs=None):
        '''initalize DecWidget '''
        dattrs = {'maxlength':3, 'size':3}
        mattrs = {'maxlength':2, 'size':2}
        sattrs = {'maxlength':5, 'size':5}
        widgets  = [
            forms.widgets.TextInput(attrs=dattrs), 
            forms.widgets.TextInput(attrs=mattrs), 
            forms.widgets.TextInput(attrs=sattrs)
        ]
        super(DecWidget,self).__init__(widgets=widgets,attrs=attrs)

    def decompress(self, value):
        if value:
            return [value.degrees, value.minutes, value.seconds]
        return [None, None, None]
            

