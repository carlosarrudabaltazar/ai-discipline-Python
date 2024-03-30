import sys;
import math;
import statistics as stat;
import matplotlib.pyplot as plt;

class FuzzyOperation (Enum):
    fuzzyAnd=1;
    fuzzyOr=2;
    fuzzyNot=3;
    
class MeaningFunction (object):
    def __init__(self,
                 realScale:list,
                 fuzzyScale:list,
                 function:str = "gauss"):
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
            case "triangle":
                return self.getTriangle(a = a,
                                        b = b,
                                        c = c);
            case "gauss":
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
        
        for key in targetMeaningFunction.keys():
            meaningFunction = targetMeaningFunction[key];
            lambdaValue = lambdaValues[key];
            
            for i in range(0, len(meaningFunction), 1):
                if i >= lambdaValue:
                    dividend += meaningFunction[i] * lambdaValue;  
                    
            divider += lambdaValue;
        
        return dividend / divider;  

def main():
    x = [0,1,2,3,4,5,6,7,8,9,10];
    y = ["ruim","bom","ótimo"];
    meaningFunction = MeaningFunction(realScale = x,
                                      fuzzyScale = y,
                                      function = "gauss");
    
    meaning = meaningFunction.getMeaningFunction();

    print(meaning["ruim"]);
    plt.plot(meaning["ruim"])
    #plt.show()
    print(meaning["bom"]);
    plt.plot(meaning["bom"])
    #plt.show()
    print(meaning["ótimo"]);
    plt.plot(meaning["ótimo"])
    plt.show()
    x = 0;

if __name__ == "__main__":
    main();