#first we need to define a constant which is the path to the redrovor package
# for now, for development purposes, we will just use a relative path above this
# but ideally we need to either move the package into site-packages, permanently
# add the path to the package to the path, or use a permanent absolute path in deployment
# in any event, if you are deploying this package, you should modify this constant to the path of 
# your redrovor package

_REDROVOR_PATH = "../../"

#now add to the path

import sys
sys.path.append(_REDROVOR_PATH)
