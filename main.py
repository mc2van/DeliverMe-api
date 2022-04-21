import json
from locationManager import *
from ga import *
from collections import namedtuple
# called by Flask API routing


def mtspDriver(locationsArray):
    parsedLocationsArray = locationsArray['locations']
    parsedCarsArray = locationsArray['cars']
    locationManager = LocationManager(parsedLocationsArray, parsedCarsArray)
    ga = GA(locationManager)
    result = ga.evolvePopulation()
    paths = [[] for _ in range(len(parsedCarsArray))]
    ind, loopTo = 0, len(parsedLocationsArray) + len(parsedCarsArray)
    while ind < loopTo:
        pathInd = result[ind]
        ind += 1
        while ind < loopTo and result[ind] >= len(parsedCarsArray):
            paths[pathInd].append(result[ind])
            ind += 1
    ret = []
    for i in range(len(parsedCarsArray)):
        curURL = "https://www.google.com/maps/dir"
        curURL += locationManager.locations[i].getAddress().replace(
                " ", "+")
        for j in paths[i]:
            curURL += "/" + locationManager.locations[j].getAddress().replace(
                " ", "+")
        if curURL == "https://www.google.com/maps/dir":
            ret.append("Car " + str(i + 1) + " has no route")
        else:
            ret.append(curURL)
    return ret


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)
