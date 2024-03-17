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
            self.targetFunction += (1/self.chromosomeSize)*((target.chromosome[i] - self.chromosome[i]) ** 2);
    
    def resetTargetFunction(self):
        self.targetFunction = 0;

    def mutate(self):
        self.chromosome[random.randint(0,self.chromosomeSize - 1)] = random.randint(0,255);

    def getWord(self) -> str:
        return ''.join(chr(gene) for gene in self.chromosome)

class Evolution (object):
    def __init__(self,
                 target:Individual):
        self.population = [];
        self.populationSize = Config().populationSize;
        self.maxGeneration = Config().maxGeneration;
        self.selectionRate = Config().selectionRate;
        self.mutationRate = Config().mutationRate;
        self.target = target;
        self.generation = 0;
        self.mutationAccumulatedProbability = random.randint(0,100) / 100;

    def startPoputation(self):
        for i in range(0, self.populationSize, 1):
            individual = Individual(i,
                                    self.target.chromosomeSize);
            individual.createChromosome();
            individual.calculateTargetFunction(self.target);
            self.population.append(individual);
            time.sleep(0.0005);
            
    def triggerMutation (self) -> bool:
        if self.mutationAccumulatedProbability < 1:
            self.mutationAccumulatedProbability += self.mutationRate;
            return False;
        else:
            self.mutationAccumulatedProbability = 0;
            return True;
        
    def crossover(self,
                  parents:list) -> list:
        newGeneration = [];
        cont = 0;
        coupleQty = int(len(parents)/2)
        maleIndividuals = parents[:coupleQty];
        femaleIndividuals = parents[coupleQty:];
                
        for i in range(0, coupleQty, 1):
            father = maleIndividuals.pop(random.randint(0,len(maleIndividuals) - 1));
            mother = femaleIndividuals.pop(random.randint(0,len(femaleIndividuals) - 1));
            halfChromosomeSize = int(father.chromosomeSize / 2);
            firstSon = Individual(cont,
                                  father.chromosomeSize);
            firstSon.createChromosome(father=father.chromosome[:halfChromosomeSize],
                                      mother=mother.chromosome[halfChromosomeSize:]);
            if self.triggerMutation():
                firstSon.mutate();
            firstSon.calculateTargetFunction(target=self.target);
            newGeneration.append(firstSon);
            cont += 1;
            secondSon = Individual(cont,
                                  father.chromosomeSize);
            secondSon.createChromosome(father=father.chromosome[halfChromosomeSize:],
                                      mother=mother.chromosome[:halfChromosomeSize]);
            if self.triggerMutation():
                secondSon.mutate();
            secondSon.calculateTargetFunction(target=self.target);
            newGeneration.append(secondSon);
            cont += 1;
                             
        return newGeneration;
    
    def truncationSelection(self) -> list:
        parents = sorted(self.population, key=lambda individual: individual.targetFunction);
        return parents[:int(self.selectionRate * self.populationSize)];
    
    def createNewGeneration(self):
        parents = self.truncationSelection();
        newGeneration = self.crossover(parents=parents);
        self.population = newGeneration + parents[:self.populationSize - len(newGeneration)];
        
    
    def getBestIndividual(self) -> Individual:
        return sorted(self.population, key=lambda individual: individual.targetFunction)[0];
    
    def start(self):
        actualGeneration = 0;
        self.startPoputation();
        
        while actualGeneration < self.maxGeneration:
            self.createNewGeneration();
            bestIndividual = self.getBestIndividual();
            print("generation: " + str(actualGeneration) + " | target: [" + ''.join(map(chr,self.target.chromosome)) + 
                  "] | best individual: [" + ''.join(map(chr,bestIndividual.chromosome)) + 
                  "] | mean squared error: " + str(bestIndividual.targetFunction));
            
            if bestIndividual.chromosome == self.target.chromosome:
                break;
            
            actualGeneration += 1;
            
            

def main():
    Targetndividual = Individual(-1);
    Targetndividual.createChromosome(target=input("Please, set de target word: "));
    evolution = Evolution(Targetndividual);
    evolution.start();
    x = 0;

if __name__ == "__main__":
    main();
