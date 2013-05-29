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
        widgets  = [forms.widgets.TextInput(), forms.widgets.TextInput(), forms.widgets.TextInput()]
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
        widgets  = [forms.widgets.TextInput(), forms.widgets.TextInput(), forms.widgets.TextInput()]
        super(DecWidget,self).__init__(widgets=widgets,attrs=attrs)

    def decompress(self, value):
        if value:
            return [value.degrees, value.minutes, value.seconds]
        return [None, None, None]
            

