import sys;
import math;
from enum import Enum;
import statistics as stat;
import matplotlib.pyplot as plt;

class FuzzyOperation (Enum):
    fuzzyAnd=1;
    fuzzyOr=2;
    fuzzyNot=3;

class FuzzyMeaningFunction (Enum):
    triangle=1;
    gauss=2;
     
class MeaningFunction (object):
    def __init__(self,
                 realScale:list,
                 fuzzyScale:list,
                 function:FuzzyMeaningFunction = FuzzyMeaningFunction.gauss):
        self.realScale = realScale;
        self.fuzzyScale = fuzzyScale;
        self.selectedFunction = function;
    
    def getMeaningFunction(self) -> dict:
        meaning = {};
        step = len(self.realScale) // (len(self.fuzzyScale) - 1);
        lastMax = 0;
        a = 0;
        b = 0;
        c = 0;

        for i in range(0, len(self.fuzzyScale),1):
            if (i == 0): 
                a = lastMax;
                b = a;
                c = lastMax + step;
                meaning[self.fuzzyScale[i]] = self.getMeaningCurve(a = a,
                                                                   b = b,
                                                                   c = c);
                lastMax = b;
            elif (i == (len(self.fuzzyScale) - 1)):
                a = ultimoMaximo;
                b = self.realScale[len(self.realScale) - 1];
                c = self.realScale[len(self.realScale) - 1];
                meaning[self.fuzzyScale[i]] = self.getMeaningCurve(a = a,
                                                                   b = b,
                                                                   c = c);
                ultimoMaximo = b;
            else:
                a = lastMax;
                b = a + step;
                c = b + step;
                meaning[self.fuzzyScale[i]] = self.getMeaningCurve(a = a,
                                                                   b = b,
                                                                   c = c);
                ultimoMaximo = b;
        return meaning;
    
    def getMeaningCurve(self,
                        a:float,
                        b:float,
                        c:float) -> list:
        match self.selectedFunction:
            case FuzzyMeaningFunction.triangle:
                return self.getTriangle(a = a,
                                        b = b,
                                        c = c);
            case FuzzyMeaningFunction.gauss:
                return self.getGauss(c = b);

    def getGauss(self,
                 c:float) -> list:
        meaning = [];
        for point in self.realScale:
            meaning.append(math.e ** ((-(1/2))*((point - c)/stat.stdev(self.realScale))**2));
        return meaning;

    def getTriangle(self,
                    a:float,
                    b:float,
                    c:float) -> list:
        meaning = [];
        for point in self.realScale:
            firstTerm = 0.0;
            secondTerm = 0.0;
            if (a == b):
                firstTerm = sys.maxsize;
            else:
                firstTerm = (point - a) / (b - a);

            if (c == b):
                secondTerm = sys.maxsize;
            else:
                secondTerm = (c - point) / (c - b);
        
            meaning.append(max(min(firstTerm, secondTerm) , 0));
        
        return meaning;
    
class FuzzyHandler (object):
        
    def fuzzify(self,
                sourceMeaningFunction:dict,
                sourceValue:int) -> dict:
        fuzzyfiedConcept = {};
        
        for key in sourceMeaningFunction.keys():
            fuzzyfiedConcept[key] = sourceMeaningFunction[key][sourceValue];
        
        return fuzzyfiedConcept;
    
    def defuzzify(self,
                  lambdaValues:dict,
                  targetMeaningFunction:dict) -> float:
        divider = 0;
        dividend = 0;
        keys = list(targetMeaningFunction.keys());
        
        for i in range(0, len(keys), 1):
            meaningFunction = targetMeaningFunction[keys[i]];
            lambdaValue = lambdaValues[keys[i]];
            descendent = False;
            for j in range(0, len(meaningFunction), 1):
                if ((i == 0) and (meaningFunction[j] <= lambdaValue)):
                    dividend += j * lambdaValue;
                    break;
                elif (i == (len(keys) - 1) and meaningFunction[j] >= lambdaValue):
                    dividend += j * lambdaValue;  
                    break;
                elif (i > 0 and i < (len(keys) - 1) and meaningFunction[j] <= lambdaValue and descendent):
                    dividend += j * lambdaValue;  
                    break;
                elif (i > 0 and meaningFunction[j] >= lambdaValue):
                    descendent = True;
                    
            divider += lambdaValue;
        
        return dividend / divider;  
    
    def fuzzyLogicOperation(self,
                            fuzzyValueA:float,
                            fuzzyOperation:FuzzyOperation,
                            fuzzyValueB:float=None) -> float:
        match fuzzyOperation:
            case FuzzyOperation.fuzzyAnd:
                return min(fuzzyValueA,fuzzyValueB);
            case FuzzyOperation.fuzzyOr:
                return max(fuzzyValueA,fuzzyValueB);
            case fuzzyOperation.fuzzyNot:
                return 1 - fuzzyValueA;