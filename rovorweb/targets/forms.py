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

    def save(self,commit=True):
        '''save the fully instantiated instance of the 
        target, looking up unknown information on simbad'''
        inst = super(ShortTargetForm,self).save(commit=False)
        if not inst.simbadName:
            inst.simbadName = simbad.getMainName(inst.name)
        if not ( inst.ra and inst.dec):
            inst.coords = simbad.getRADec(inst.name)
        if commit:
            inst.save()
        return inst

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
