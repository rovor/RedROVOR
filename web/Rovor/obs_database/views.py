# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def upload_form(request):
    '''form fo uploading observation from a folder on the server''' 
    return render(request,'obs_database/upload_form.html')

