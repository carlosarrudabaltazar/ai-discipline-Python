import yaml;
import random;
import math;
import time;

class Config (object):
    _instance = None
    def __init__(self):
        with open("ga_config.yaml") as stream:
            try:
                yamlConfig = yaml.safe_load(stream);
                self.mutationRate = yamlConfig["mutationRate"];
                self.populationSize = yamlConfig["populationSize"];
                self.maxGeneration = yamlConfig["maxGeneration"];
                self.selectionRate = yamlConfig["selectionRate"];
            except yaml.YAMLError as exc:
                print(exc);

    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

class Individual (object):
    def __init__(self,
                 id:int,
                 chromosomeSize:int = None):
        self.id = id;
        self.chromosomeSize = chromosomeSize;
        self.chromosome = [];
        self.targetFunction = 0;
        self.rouletteProportion = 0.0;
        self.mutationRate = Config().mutationRate;

    def createChromosome (self,
                          target:str=None,
                          father:list=[],
                          mother:list=[]):
        if not(target is None):
            self.chromosome = [ord(char) for char in target];
            self.chromosomeSize = len(self.chromosome);
        elif ((len(father)) != 0 and (len(mother) != 0)):
            self.chromosome = father + mother;
        else:
            for i in range(0, self.chromosomeSize, 1):
                self.chromosome.append(random.randint(0,255));

    def calculateTargetFunction(self,
                                target:object):
        for i in range(0, len(target.chromosome),1):
            self.targetFunction += math.sqrt((target.chromosome[i] - self.chromosome[i]) ** 2);
    
    def resetTargetFunction(self):
        self.targetFunction = 0;

    def mutate(self):
        self.chromosome[random.randint(0,len(self.chromosome) - 1)] = random.randint(0,255);

    def getWord(self) -> str:
        return ''.join(chr(gene) for gene in self.chromosome)

class Evolution (object):
    def __init__(self,
                 target:Individual):
        self.population = [];
        self.populationSize = Config().populationSize;
        self.maxGeneration = Config().maxGeneration;
        self.selectionRate = Config().selectionRate;
        self.target = target;
        self.generation = 0;

    def startPoputation(self):
        for i in range(0, self.populationSize, 1):
            individual = Individual(self.target.chromosomeSize);
            individual.createChromosome();
            individual.calculateTargetFunction(self.target);
            self.population.append(individual);
            time.sleep(0.005);

    def rouletteSelection(self):
        self.population = sorted(self.population, key=lambda individual: individual.targetFunction);
        tfSomatory = sum(individual.targetFunction for individual in self.population);

        x = 0;
        



def main():
    Targetndividual = Individual();
    Targetndividual.createChromosome(target=input("Please, set de target word: "));
    evolution = Evolution(Targetndividual);
    evolution.startPoputation();
    evolution.rouletteSelection();
    x = 0;

if __name__ == "__main__":
    main();
