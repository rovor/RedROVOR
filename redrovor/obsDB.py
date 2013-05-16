#!/usr/bin/python

import cookielib, urllib2
import hashlib
import json

from urllib import urlencode

import logging

logger = logging.getLogger("Rovor.obsdb")

class ObsDBError(Exception):
    def __init__(self,origError,page='', request=''):
        self.origError = origError
        self.page=page
        self.request=request
    def __str__(self):
        return 'Error: {0}\nPage:{1}\nRequest{2}\n'.format(
            self.origError, self.page, self.request)

jar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

username='rovor' #username for the database
passwordHash =hashlib.sha1('0uth0us3').hexdigest() #password hash for the database

loginRequest = {'command':'login','uname':username,'pword':passwordHash}

baseurl='http://rovor.byu.edu/obs_database/'

def _url(page):
    '''create the full url for a page on the database'''
    return baseurl+page

def _sendRequest(page,reqObj=None):
    if reqObj is not None:
        reqObj = urlencode(reqObj)
    try:
        res = opener.open(_url(page), reqObj).read()
        #return json.load(res)
        return json.loads(res)
    except Exception as e:
        raise ObsDBError(e,page=page, request=reqObj)

def login():
    return _sendRequest('login_request.php',loginRequest)

def logout():
    return _sendRequest('login_request.php?command=logout')

def is_loggedIn():
    return _sendRequest('login_request.php?command=is_loggedIN')

def is_admin():
    return _sendRequest('login_request.php?command=is_admin')

def addObject(name,types=None, otherNames=None):
    reqObj = {'command':'add','name':name}
    if types is not None:
        reqObj['types']=types
    if otherNames is not None:
        reqObj['otherNames'] = otherNames
    return _sendRequest('object_request2.php', reqObj)

def obj_get_or_add(name):
    return _sendRequest('object_request2.php',{'command':'get_or_add','name':name})

def get_objs(orderby=None, limit=None):
    reqObj = {'command':'getObjs'}
    if orderby is not None:
        reqObj['orderby']=orderby
    if limit is not None:
        reqObj['limit']=limit
    return _sendRequest('object_request2.php',reqObj)

def update_obj(ID,name, otherNames, types):
    reqObj = {'command': 'update', 'id':ID, 'otherNames':otherNames, 'types':types}
    return _sendRequest('object_request2.php',reqObj)

def delete_obj(ID):
    return _sendRequest('object_request2.php', {'command': 'delete', 'id':ID})

def obj_search(query):
    return _sendRequest('object_request2.php', {'command':'search', 'q':query})

def lookup_name(ra,dec):
    return _sendRequest('object_request2.php', {'command':'nameLookup', 'ra':ra, 'dec':dec})

# observation commands

def newObservation(obj_id, utdate, ffilter, exptime, temp, nframes=1, fname='', notes=''):
    '''Log a new observation'''
    return _sendRequest('obs_request2.php',{'command':'new','object_id':obj_id, 'utdate':utdate,
        'filter':ffilter,'exptime':exptime, 'temp':temp, 'nframes':nframes, 
        'filename':fname, 'notes':notes})

def getObsFull(orderby='utdate',limit=None, **kwfilter):
    req = {'command':'getObsFull', 'orderby':orderby}
    if limit is not None:
        req['limit'] = limit
    if kwfilter:
        req['filter']=kwfilter
    return _sendRequest('obs_request2.php',req)
    
