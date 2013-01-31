from collections import defaultdict
import json


class observationSummary :
    '''basically a wrapper around a dictionary mapping the 
    name of the target to a dictionary mapping the filter type to the number
    of images in that filter'''
    def __init__(self):
        #initialize the rather complicated underlying data structure
        #we use defaultdict to make it easier to increment stuff
        self._data = defaultdict(lambda: defaultdict(lambda:0))
        return
    def addObservation(self, targetName, ifilter):
        '''record a new observation of targetName, in filter ifilter
        i.e. increment the count of that name and filter, return the new count'''
        self._data[targetName][ifilter] += 1
        return self._data[targetName][ifilter]
    def __getitem__(self, targetName):
        '''return a dictionary mapping filter type to number in that filter'''
        return self._data[targetName]
    def __len__(self):
        return len(_data)
    def __iter__(self):
        '''iterate over targetNames'''
        return iter(self._data)
    def iteritems(self):
        '''iterate over all targetName, filter combinations'''
        for (targetName, ifilters) in self._data.iteritems():
            for (ifilter, num) in ifilters_.iteritems():
                yield( targetName, ifilters, num)
    def getJson(self):
        '''get the json string for the dictionary'''
        return json.dumps(self._data)
    def __str__(self):
        '''the string representation will be:
        targetName:
                filterName  num
        repeated for each targetname'''
        return '\n'.join(map( lambda terms: '%s:\n\t%s %d' % terms, self.iteritems()))



