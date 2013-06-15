from targets.models import Target, FieldObject
from redrovor.thirdpass import ThirdPassProcessor


def getObjectMapping(path):
    '''create temporary coordinate files
    and return them in the appropriate mapping for the
    ThirdPassProcessor to phot, (i.e. mapping from objectname to 
    tuple of coordinate file path, and target coordinates).

    @returns a tuple of the object mapping, and a list of object names
    which we currently don't have any coordinates for.
    '''
    improc = ThirdPassProcessor(path)
    objs_needed = improc.objectNames()
    mapping = {}
    missing = []
    for name in objs_needed:
        target = Target.objects.filter(simbadName=name)
        if target and target[0].hasCoordinates():
            mapping[name] = ( target[0].tempCoordFile(), target[0].coords )
        else:
            missing.append(name)
    return (mapping,missing)

        


