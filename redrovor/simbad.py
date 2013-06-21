from urllib import urlopen,urlencode
from coords import RA_coord, Dec_coord,Coords
from decimal import Decimal
import re

SIMBAD_URL = "http://simbad.u-strasbg.fr/simbad/"
SIMBAD_SCRIPT_URL = SIMBAD_URL + "/sim-script"



def script_request(script):
    '''run a simbad script and return the result as an array
    of strings (each item is a single line of the output),
    this uses caching to improve performance'''
    #first prepend a line to quiet the console and script echo
    script = "output console=off script=off\n" + script
    resource = urlopen(SIMBAD_SCRIPT_URL, urlencode({'script':script}))
    result = [x.strip() for x in resource if x.strip()] 
    resource.close()
    return result


def getAllNamesFromName(name):
    '''return an array of all names for an object in simbad'''
    script = r'''format object "%IDLIST[%*(S)\n]"
    query id {0}'''.format(name)
    return script_request(script)


def getNamesFromRADec(ra,dec,radius='5m'):
    '''get the names of objects with radius of ra and dec.
    we expect ra and dec to be RA_coord and Dec_coord objects
    or at least to be convertable by string to the normal
    colon delimited sexigesimal format'''
    script = r'''format object "%IDLIST[%*(S)\n]"
    query coo {0:s} {1:s} radius={2:s}'''.format(ra,dec,radius)
    return script_request(script)


def getRADec(name):
    '''get a Coords object for the given object'''
    script = r'''format object "%COO(:s;A | D)"
    query id {0}'''.format(name)
    result = script_request(script)
    if ':error:' in result[0]:
        return None
    ra,dec = result[0].split('|')
    ra = RA_coord.fromStr(ra.strip())
    match = getRADec._min_re.match(dec.strip())
    if match:
        #we need to take care of the special case when we get fractional minutes instead of seconds
        d = int(match.group(1))
        mins = Decimal(match.group(2))
        m = int(mins)
        s = (mins-m)*60
        dec = Dec_coord(d,m,s)
    else:
        dec = Dec_coord.fromStr(dec.strip())
    return Coords(ra,dec)

getRADec._min_re = re.compile(r'^([+-]?\d+):(\d+\.?\d*)$')

def getMainName(name):
    '''get the "main" name for the given object in simbad,
    useful for uniquely identifying an object
    if the name wasn't found return the name that was passed in'''
    if name in getMainName.cache:
        return getMainName.cache[name]
    script = r'''format object "%IDLIST(1)[%*(S)]"
    query id {0}'''.format(name)
    response = script_request(script)
    if ':error:' in response[0]:
        #error, so just return the name that was given to us
        result = name
    else:
        result = response[0]
    getMainName.cache[name] = result
    return result
getMainName.cache = {}

