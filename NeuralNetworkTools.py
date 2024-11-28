from enum import Enum;
import pandas as pd;
import math;
import operator;

class ActivationFunctions (Enum):
    stepFunction = 1;
    stepNegativeFunction = 2;
    linearFunction = 3;
    sigmoidFunction = 4;
    tanhFunction = 5;
    reLUFunction = 6;
    leakyreLUFunction = 7;
    
class TrainRules (Enum):
    deltaRule = 1;

class ActivationFunction (object):
    def __init__(self,
                 theta:float=None):
        self.theta = theta;
        
    def getStep (self,
                 summation:float) -> float:
        if summation >= self.theta:
            return 1;
        else:
            return 0;

    def getNegativeStep(self,
                        summation:float) -> float:
        if summation >= self.theta:
            return 1;
        else:
            return -1;

    def getLinear(self,
                  summation:float) -> float:
        return summation;
    
    def getSigmoid(self,
                   summation:float) -> float:
        return 1 / (1 + (math.e ** (summation * -1)));
    
    def getTanh(self,
                summation:float) -> float:
        return (math.e ** summation - math.e ** (summation * -1)) / (math.e ** summation + math.e ** (summation * -1));
    
    def getreLU(self,
                summation:float) -> float:
        return max(summation, 0);
    
    def getLeakyreLU(self,
                     summation:float) -> float:
        return max((summation * 0.1),summation);

class Neuron (ActivationFunction):
    def __init__(self,
                 theta:float=None,
                 activationFunction:ActivationFunctions=ActivationFunctions.stepFunction):
        super().__init__(theta = theta);
        self.activationFunction = activationFunction;

    def getActivation(self,
                      x:list,
                      w:list) -> float:

        summation = sum(list(map(operator.mul, x, w)));
        match self.activationFunction:
            case ActivationFunctions.stepFunction:
                return super().getStep(summation);
            case ActivationFunctions.stepNegativeFunction:
                return super().getNegativeStep(summation);
            case ActivationFunctions.linearFunction:
                return super().getLinear(summation);
            case ActivationFunctions.sigmoidFunction:
                return super().getSigmoid(summation);
            case ActivationFunctions.tanhFunction:
                return super().getTanh(summation);
            case ActivationFunctions.reLUFunction:
                return super().getreLU(summation);
            case ActivationFunctions.leakyreLUFunction:
                return super().getLeakyreLU(summation);
            
class Train (object):
    def __init__(self,
                 neuron:Neuron,
                 trainSample:pd.DataFrame,
                 w:list,
                 eta:float,
                 acceptableError:float=0,
                 trainRule:TrainRules=TrainRules.deltaRule):
        self.neuron = neuron;
        self.trainSample = trainSample;
        self.w = w;
        self.trainRule = trainRule;
        self.eta = eta;
        self.accetableError = acceptableError;
        
    def train(self,
              verbose:bool=False) -> list:
        y = None;
        globalError = None;
        epoch = 0;

        while globalError != self.accetableError:
            globalError = 0;
            localErrors = [];

            for i in range(0, self.trainSample[self.trainSample.columns[0]].count(),1):
                x = self.trainSample.iloc[i,0:len(self.trainSample.columns)-1].tolist();
                yd = self.trainSample.iloc[i,len(self.trainSample.columns)-1];
                y = self.neuron.getActivation(x=x,
                                              w=self.w);
                
                match self.trainRule:
                    case TrainRules.deltaRule:
                        self.w = self.getDeltaRuleCorrection(x=x,
                                                             w=self.w,
                                                             eta=self.eta,
                                                             y=y,
                                                             yd=yd);
    
                localErrors.append(yd - y);

            for error in localErrors:
                globalError -= error**2;
    
            if verbose:
                print("\tEpoch (" + str(epoch) +"): f(e) = " + str(globalError));
                print("\tNew weight set: " + str(self.w) + "\n\n");
    
            epoch += 1;

        return self.w;


    def getDeltaRuleCorrection(self,
                               x:list,
                               w:list,
                               eta:float,
                               y:float,
                               yd:float) -> list:
        newWeights = [];

        for i in range(0, len(x), 1):
            newWeights.append(w[i] + eta * (yd - y) * x[i]);

        return newWeights;