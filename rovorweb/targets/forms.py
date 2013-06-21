from django import forms
from redrovor import simbad
from models import Target, CoordFileModel
from form_fields import RAField, DecField



#forms for the models

class TargetForm(forms.ModelForm):
    class Meta:
        model = Target

class ShortTargetForm(forms.ModelForm):
    ra = RAField(label='Right Ascension',required=False)
    dec = DecField(label='Declination', required=False)

    class Meta:
        model = Target
        fields=['name','ra','dec']

class TargetNameOnlyForm(forms.ModelForm):
    class Meta:
        model = Target
        fields=['name']

class CoordFileModelForm(forms.ModelForm):
    class Meta:
        model = CoordFileModel
