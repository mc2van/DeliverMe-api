from locationManager import *
from genes import *


class Population:
    def __init__(self, locationManager, n):
        # n is size of population
        self.size = n
        self.genesList = []
        self.locationManager = locationManager
        for i in range(n):
            self.genesList.append(Gene(
                self.locationManager))
        self.probabilityList = self.calcProbability()

    def calcProbability(self):
        totalFitness = 0
        res = []
        for gene in self.genesList:
            totalFitness += gene.fitnessScore
        for i in range(self.size):
            res.append(
                self.genesList[i].fitnessScore / totalFitness)
        return res

    def findTotalFitness(self):
        res = 0
        for gene in self.genesList:
            res += gene.fitness()
        self.totalFitness = res
