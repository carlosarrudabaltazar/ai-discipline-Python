import sys;
import math;
import statistics as stat;
import matplotlib.pyplot as plt;

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
        d = 0;

        for i in range(0, len(self.fuzzyScale),1):
            if (i == 0): 
                a = (lastMax + step) / 2;
                b = a;
                c = lastMax + step;
                d = c + b;
                meaning[self.fuzzyScale[i]] = self.getMeaningCurve(a=a,
                                                                   b=b,
                                                                   c=c,
                                                                   d=d);
                lastMax = b;
            elif (i == (len(self.fuzzyScale) - 1)):
                a = ultimoMaximo;
                b = self.realScale[len(self.realScale) - 1];
                c = self.realScale[len(self.realScale) - 1];
                d = ultimoMaximo;
                meaning[self.fuzzyScale[i]] = self.getMeaningCurve(a=a,
                                                                   b=b,
                                                                   c=c,
                                                                   d=d);
                ultimoMaximo = b;
            else:
                a = lastMax;
                b = lastMax + step;
                c = b + step;
                d = lastMax;
                meaning[self.fuzzyScale[i]] = self.getMeaningCurve(a=a,
                                                                   b=b,
                                                                   c=c,
                                                                   d=d);
                ultimoMaximo = b;
        return meaning;
    
    def getMeaningCurve(self,
                        a:float,
                        b:float,
                        c:float,
                        d:float) -> list:
        match self.selectedFunction:
            case "triangle":
                return self.getTriangle(a=a,
                                        b=b,
                                        c=c);
            case "gauss":
                return self.getGauss(c=c);
            case "trapezium":
                return self.getTrapezium(a=a,
                                         b=b,
                                         c=c,
                                         d=d);

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

    def getTrapezium(self,
                     a:float,
                     b:float,
                     c:float,
                     d:float) -> list:
        meaning = [];
        for point in self.realScale:
            firstTerm = 0.0;
            secondTerm = 0.0;
            if (a == b):
                firstTerm = sys.maxsize;
            else:
                firstTerm = (point - a) / (b - a);

            if (c == d):
                secondTerm = sys.maxsize;
            else:
                secondTerm = (d - point) / (d - c);
        
            meaning.append(max(min(firstTerm, 1, secondTerm), 0));
        
        return meaning;

def main():
    x = [0,1,2,3,4,5,6,7,8,9,10];
    y = ["ruim","bom","ótimo"];
    meaningFunction = MeaningFunction(realScale = x,
                                      fuzzyScale = y,
                                      function="trapezium");
    
    z = meaningFunction.getTrapezium(0,0,2.5,5);
    plt.plot(z)
    plt.show()
    
    meaning = meaningFunction.getMeaningFunction();

    print(meaning["ruim"]);
    plt.plot(meaning["ruim"])
    plt.show()
    print(meaning["bom"]);
    plt.plot(meaning["bom"])
    plt.show()
    print(meaning["ótimo"]);
    plt.plot(meaning["ótimo"])
    plt.show()
    x = 0;

if __name__ == "__main__":
    main();