class Location:
    def __init__(self, address, coords, index):
        self.address = address
        self.coords = coords
        self.index = index

    def getAddress(self):
        return self.address

    def getCoords(self):
        return self.coords

    def getLatitude(self):
        return self.coords['lat']

    def getLongitude(self):
        return self.coords['long']

    def getIndex(self):
        return self.index
