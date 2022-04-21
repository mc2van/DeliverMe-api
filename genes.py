from locationManager import *
import random
import numpy as np


class Gene:
    def __init__(self, locationManager):
        self.locationManager = locationManager
        self.n = locationManager.n
        self.m = locationManager.m
        self.numList = [i for i in range(1, self.n + self.m)]
        random.shuffle(self.numList)
        self.numList = [0] + self.numList
        self.fitnessScore = self.fitness()

    def fitness(self):
        ind = 0
        paths = [[] for _ in range(self.m)]
        while ind < self.n + self.m:
            pathInd = self.numList[ind]
            ind += 1
            while ind < self.n + self.m and self.numList[ind] >= self.m:
                paths[pathInd].append(self.numList[ind])
                ind += 1
        pathDists = [self.pathDist(i, paths[i]) for i in range(self.m)]
        return sum(pathDists) + (0.9 * (max(pathDists) - min(pathDists)))

    def pathDist(self, index, path):
        if not len(path):
            return 0
        pathLen = sum(self.locationManager.getDist(
            path[i], path[i + 1]) for i in range(len(path) - 1))
        return self.locationManager.getDist(index, path[0]) + self.locationManager.getDist(index, path[-1]) + pathLen

    def clone(self):
        res = Gene(self.locationManager)
        res.numList = self.numList.copy()
        return res

    def mutate(self):
        if self.m == 1:
            bounds = sorted([random.randint(1, self.m + self.n),
                            random.randint(1, self.m + self.n)])
            snippet = []
            for i in range(bounds[0], bounds[1]):
                snippet.append(self.numList[i])
            for i in range(bounds[0], bounds[1]):
                self.numList[i] = snippet.pop()
            self.fitnessScore = self.fitness()
        else:
            typeOfMutation = random.randint(1, 2)
            invert = random.randint(0, 1)
            if typeOfMutation == 1:
                toReallocate = random.randint(0, self.m)
                low = self.numList.index(toReallocate) + 1
                ind = low
                while ind < self.n + self.m and self.numList[ind] >= self.m:
                    ind += 1
                high = ind
                first = random.randint(low, high)
                second = random.randint(low, high)
                bounds = sorted([first,
                                second])
                toReceive = random.randint(0, self.m + self.n - 1)
                while bounds[0] <= toReceive <= bounds[1]:
                    toReceive = random.randint(0, self.m + self.n - 1)
                res = []
                ind = 0
                arr = np.asarray(self.numList)
                arrToMove = arr[bounds[0]:bounds[1]]
                np.delete(arr, np.s_[bounds[0]:bounds[1]:1], None)
                np.insert(arr, toReceive + 1, arrToMove, None)
                arr.flatten()
                self.numList = arr.tolist()
                self.fitnessScore = self.fitness()
            if typeOfMutation == 2:
                firstPath = random.randint(0, self.m)
                secondPath = random.randint(0, self.m)
                firstLength, firstIndex, secondLength, secondIndex = 0, 0, 0, 0
                for i in range(self.n + self.m):
                    if self.numList[i] == firstPath:
                        firstIndex = i
                        firstLength += 1
                        i += 1
                        while i < len(self.numList) and self.numList[i] >= self.m:
                            firstLength += 1
                            i += 1
                for i in range(self.n + self.m):
                    if self.numList[i] == secondPath:
                        secondIndex = i
                        secondLength += 1
                        i += 1
                        while i < len(self.numList) and self.numList[i] >= self.m:
                            secondLength += 1
                            i += 1
                firstFirst = random.randint(
                    firstIndex, firstIndex + firstLength - 1 if firstIndex + firstLength - 1 != firstIndex else firstIndex + 1)
                firstSecond = random.randint(
                    firstIndex, firstIndex + firstLength - 1 if firstIndex + firstLength - 1 != firstIndex else firstIndex + 1)
                firstBounds = sorted([firstFirst,
                                      firstSecond])
                secondFirst = random.randint(
                    secondIndex, secondIndex + secondLength - 1 if secondLength != 1 else secondIndex + 1)
                secondSecond = random.randint(
                    secondIndex, secondIndex + secondLength - 1 if secondIndex + secondLength - 1 != secondIndex else secondIndex + 1)
                secondBounds = sorted([secondFirst,
                                       secondSecond])
                i = 0
                arr = np.asarray(self.numList)
                arrToMove1 = arr[firstBounds[0]:firstBounds[1]]
                arrToMove2 = arr[secondBounds[0]:secondBounds[1]]
                if (firstBounds[0] < secondBounds[0]):
                    np.delete(arr, np.s_[secondBounds[0]                              :secondBounds[1]:1], None)
                    np.insert(arr, secondBounds[0], arrToMove1, None)
                    np.delete(arr, np.s_[firstBounds[0]                              :firstBounds[1]:1], None)
                    np.insert(arr, firstBounds[0], arrToMove2, None)
                else:
                    np.delete(arr, np.s_[firstBounds[0]                              :firstBounds[1]:1], None)
                    np.insert(arr, firstBounds[0], arrToMove2, None)
                    np.delete(arr, np.s_[secondBounds[0]                              :secondBounds[1]:1], None)
                    np.insert(arr, secondBounds[0], arrToMove1, None)
                arr.flatten()
                self.numList = arr.tolist()
