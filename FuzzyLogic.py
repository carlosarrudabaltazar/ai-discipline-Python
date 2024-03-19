import sys;
import math;
import statistics as stat;
import matplotlib.pyplot as plt;

class PertinenceFunction (object):
    def __init__(self,
                 realScale:list,
                 a:float,
                 b:float,
                 c:float,
                 d:float = None):
        self.realScale = realScale;
        self.a = a;
        self.b = b;
        self.c = c;
        self.d = d;

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

def main():
    x = [0,1,2,3,4,5,6,7,8,9,10];
    pertinence = PertinenceFunction(realScale = x,
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