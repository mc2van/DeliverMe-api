from location import *


class LocationManager:
    def __init__(self, locationsList, carInitList):
        self.n = len(locationsList)
        self.m = len(carInitList)
        self.locations = []
        for i in range(len(carInitList)):
            location = carInitList[i]
            newLocation = Location(location['address'], location['coords'], i)
            self.locations.append(newLocation)
        for i in range(len(locationsList)):
            location = locationsList[i]
            newLocation = Location(location['address'], location['coords'], i)
            self.locations.append(newLocation)

        self.distMatrix = []
        for i in range(len(self.locations)):
            self.distMatrix.append([])
            for j in range(len(self.locations)):
                dist = abs(self.locations[i].coords['lat'] -
                           self.locations[j].coords['lat']) + abs(self.locations[i].coords['long'] -
                                                                  self.locations[j].coords['long'])
                self.distMatrix[i].append(dist)

    def getDist(self, location1, location2):
        return self.distMatrix[location1][location2]

    def getLocation(self, index):
        return self.locations[index]
