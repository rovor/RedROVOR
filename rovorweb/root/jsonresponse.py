import json

from django.http import HttpResponse

def okJSONResponse(res=None):
    '''return an httpresponse encapsulating a json object
    with two properties, ok and result where ok is true
    and result is the JSON representation of result'''
    return HttpResponse(json.dumps({'ok':True, 'result':res}),mimetype='application/json')

def errorJSONResponse(err):
    '''return an httpresponse encapsulating a json object
    with two properties, ok and error where ok is true
    and error is the JSON representation of err'''
    return HttpResponse(json.dumps({'ok':False, 'error':err}))
