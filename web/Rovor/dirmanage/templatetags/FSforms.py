from django import template
from django.template.loader import get_template

register = template.Library()



@register.inclusion_tag('dirmanage/frameChooserDialog.html')
def frameChooserDialog(id,callback,startPath="Raw/"):
    '''template tag for a modal dialog which
    allows the user to select one or more FITS images.
    This is intended for use in other forms'''
    return {'id':id, 'callback':callback,'startPath':startPath}



