from django import template
from django.template.loader import get_template

register = template.Library()



@register.inclusion_tag('dirmanage/frameChooserDialog.html')
def frameChooserDialog(id,callback,startPath="Raw/"):
    '''template tag for a modal dialog which
    allows the user to select one or more FITS images.
    This is intended for use in other forms'''
    return {'id':id, 'callback':callback,'startPath':startPath}

@register.inclusion_tag('dirmanage/dirChooserDialog.html')
def dirChooserDialog(id,callback,startPath="Raw/"):
    '''template tag for a modal dialog which allows
    the user to select a directory (folder). Only one (sorry)
    This is intended for use in other forms'''
    return {'id':id, 'callback':callback, 'startPath':startPath}

@register.inclusion_tag('dirmanage/fileChooserDialog.html')
def fileChooserDialog(id,callback,startPath="Raw/"):
    '''template tag for a modal dialog which allows
    the user to select a single file. Only one (sorry)
    This is intended for use in other forms'''
    return {'id':id, 'callback':callback, 'startPath':startPath}

@register.inclusion_tag('dirmanage/browseTag.html')
def twoFrameBrowse(id,startPath='',js_name=None):
    '''template tag for use in twoFrameBrowser.html and children
    to put a two-frame browser in place, with id = id
    and initilaly with a top path of startPath. 
    By default it create a BroswerWindow object named id,
    but the name of the BrowserWindow object can be overriden by 
    passing in a value to js_name'''
    return {'id':id, 'startPath':startPath, 'js_name': js_name or id}




