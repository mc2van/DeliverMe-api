from locationManager import *
from genes import *
from population import *
import random
from numpy.random import choice

POPULATION_SIZE = 100
NUM_EVOLUTIONS = 30


class GA:
    def __init__(self, locationManager):
        self.locationManager = locationManager

    def evolvePopulation(self):
        independentPopulations = [Population(
            self.locationManager, POPULATION_SIZE) for _ in range(5)]
        for i in range(5):
            for j in range(NUM_EVOLUTIONS):
                self.doEvolve(independentPopulations[i])
        finalPopulationGenesList = []
        for i in range(5):
            finalPopulationGenesList += [
                i for i in independentPopulations[i].genesList]
        finalPopulationGenesList = sorted(
            finalPopulationGenesList, key=lambda x: x.fitnessScore)[:POPULATION_SIZE]
        finalPopulation = Population(self.locationManager, POPULATION_SIZE)
        finalPopulation.size = POPULATION_SIZE
        finalPopulation.genesList = finalPopulationGenesList
        finalPopulation.locationManager = self.locationManager
        finalPopulation.probabilityList = finalPopulation.calcProbability()
        for i in range(NUM_EVOLUTIONS):
            self.doEvolve(finalPopulation)
        testRes = []
        for gene in finalPopulation.genesList:
            testRes.append(gene.fitnessScore)
        return finalPopulation.genesList[0].numList

    # returns new gene with crossover x+y
    # x and y are numLists for two genes
    def crossover(self, x, y, sz):
        bounds = sorted([random.randint(0, sz), random.randint(0, sz)])
        res = [-1] * sz
        chunk = [0] * sz
        for i in range(bounds[0], bounds[1]):
            chunk[x.numList[i]] = 1
            res[i] = x.numList[i]
        ind, nxt = 0, 0
        while ind < sz:
            while ind < sz and res[ind] != -1:
                ind += 1
            while nxt < sz and chunk[y.numList[nxt]]:
                nxt += 1
            if ind < sz and nxt < sz:
                res[ind] = y.numList[nxt]
                nxt += 1
                ind += 1
        resGene = x.clone()
        resGene.numList = res
        resGene.fitnessScore = resGene.fitness()
        return resGene

    def doEvolve(self, population):
        # cross over
        temp = []
        for i in range(POPULATION_SIZE):
            parents = self.chooseParents(population)

            temp.append(self.crossover(
                parents[0], parents[1], len(parents[0].numList)))
        for thing in temp:
            population.genesList.append(thing)
        for i in range(len(population.genesList)):
            if random.randint(0, 100) < 30:
                population.genesList.append(population.genesList[i].clone())
                population.genesList[i].mutate()
        population.probabilityList = population.calcProbability()
        population.genesList.sort(key=lambda x: x.fitnessScore)
        population.genesList = population.genesList[:POPULATION_SIZE]
        population.probabilityList = population.calcProbability()
        return

    def chooseParents(self, population):
        parent1 = choice(population.genesList, p=population.probabilityList)
        parent2 = choice(population.genesList, p=population.probabilityList)
        while parent2 == parent1:
            parent2 = choice(population.genesList,
                             p=population.probabilityList)
        return [parent1, parent2]
