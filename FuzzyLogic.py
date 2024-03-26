import sys;
import math;
import statistics as stat;
import matplotlib.pyplot as plt;

class MeaningCurve (object):
    def __init__(self,
                 realScale:list,
                 a:float,
                 b:float,
                 c:float,
                 d:float = None,
                 function:str = "gauss"):
        self.realScale = realScale;
        self.a = a;
        self.b = b;
        self.c = c;
        self.d = d;
        self.selectedFunction = function;
    
    def getMeaningCurve(self) -> list:
        match self.selectedFunction:
            case "triangle":
                return self.getTriangle();
            case "gauss":
                return self.getGauss();
            case "trapezium":
                return self.getTrapezium();

    def getGauss(self) -> list:
        pertinence = [];
        for point in self.realScale:
            pertinence.append(math.e ** ((-(1/2))*((point - self.c)/stat.stdev(self.realScale))**2));
        return pertinence;

    def getTriangle(self) -> list:
        pertinence = [];
        for point in self.realScale:
            firstTerm = 0.0;
            secondTerm = 0.0;
            if (self.a == self.b):
                firstTerm = sys.maxsize;
            else:
                firstTerm = (point - self.a) / (self.b - self.a);

            if (self.c == self.b):
                secondTerm = sys.maxsize;
            else:
                secondTerm = (self.c - point) / (self.c - self.b);
        
            pertinence.append(max(min(firstTerm, secondTerm) , 0));
        
        return pertinence;

    def getTrapezium(self) -> list:
        pertinence = [];
        for point in self.realScale:
            firstTerm = 0.0;
            secondTerm = 0.0;
            if (self.a == self.b):
                firstTerm = sys.maxsize;
            else:
                firstTerm = (point - self.a) / (self.b - self.a);

            if (self.c == self.b):
                secondTerm = sys.maxsize;
            else:
                secondTerm = (self.d - point) / (self.d - self.c);
        
            pertinence.append(max(min(firstTerm, 1, secondTerm) , 0));
        
        return pertinence;

class MeaningFunction (object):
    def __init__(self,
                 realScale:list,
                 fuzzyScale:list):
        self.realScale = realScale;
        self.fuzzyScale = fuzzyScale;

    def getMeaningFunction(self,
                           function:str="gauss"):
        meaningFunction = {};
        step = len(self.realScale) // (len(self.fuzzyScale) - 1);
        lastMax = 0;
        a = 0;
        b = 0;
        c = 0;
        d = 0;

        for i in range(0, len(self.fuzzyScale),1):
            if (i == 0): 
                a = lastMax;
                b = lastMax;
                c = lastMax + step;
                meaningCurve = MeaningCurve(realScale=self.realScale,
                                            a=a,
                                            b=b,
                                            c=c,
                                            function=function);
                meaningFunction[self.fuzzyScale[i]] = meaningCurve.getMeaningCurve();
                lastMax = b;
            elif (i == (len(self.fuzzyScale) - 1)):
                a = ultimoMaximo;
                b = self.realScale[len(self.realScale) - 1];
                c = self.realScale[len(self.realScale) - 1];
                meaningCurve = MeaningCurve(realScale=self.realScale,
                                            a=a,
                                            b=b,
                                            c=c,
                                            function=function);
                meaningFunction[self.fuzzyScale[i]] = meaningCurve.getMeaningCurve();
                ultimoMaximo = b;
            else:
                a = lastMax;
                b = lastMax + step;
                c = b + step;
                meaningCurve = MeaningCurve(realScale=self.realScale,
                                            a=a,
                                            b=b,
                                            c=c,
                                            function=function);
                meaningFunction[self.fuzzyScale[i]] = meaningCurve.getMeaningCurve();
                ultimoMaximo = b;


def main():
    x = [0,1,2,3,4,5,6,7,8,9,10];
    pertinence = MeaningFunction(realScale = x,
                                 a = 5,
                                 b = 10,
                                 c = 10);
    print(pertinence.getGauss());
    plt.plot(pertinence.getGauss())
    plt.show()
    print(pertinence.getTriangle());
    plt.plot(pertinence.getTriangle())
    plt.show()
    x = 0;

if __name__ == "__main__":
    main();