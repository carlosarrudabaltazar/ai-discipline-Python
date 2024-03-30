from enum import Enum;
import math;
import operator;
import time;

class ActivationFunctions (Enum):
    stepFunction = 1;
    linearFunction = 2;
    sigmoidFunction = 3;
    tanhFunction = 4;
    reLUFunction = 5;
    leakyreLUFunction = 6;
    
class TrainRules (Enum):
    deltaRule = 1;

class ActivationFunction (object):
    def __init__(self,
                 sum:float,
                 theta:float=None):
        self.sum = sum;
        self.theta = theta;
        
    def getStep (self) -> float:
        if self.sum >= self.theta:
            return 1;
        else:
            return 0;
        
    def getLinear(self) -> float:
        return self.sum;
    
    def getSigmoid(self) -> float:
        return 1 / (1 + (math.e ** (self.sum * -1)));
    
    def getTanh(self) -> float:
        return (math.e ** self.sum - math.e ** (self.sum * -1)) / (math.e ** self.sum + math.e ** (self.sum * -1));
    
    def getreLU(self) -> float:
        return max(self.sum, 0);
    
    def getLeakyreLU(self) -> float:
        return max((self.sum * 0.1),self.sum);

class MCPNeuron (ActivationFunction):
    def __init__(self,
                 x:list,
                 w:list,
                 theta:float=None,
                 activationFunction:ActivationFunctions=ActivationFunctions.stepFunction):
        self.sum = sum(list(map(operator.mul, x, w)));
        super().__init__(sum = self.sum,
                         theta = theta);
        self.activationFunction = activationFunction;

    def getActivation(self) -> float:
        match self.activationFunction:
            case ActivationFunctions.stepFunction:
                return super().getStep();
            case ActivationFunctions.linearFunction:
                return super().getLinear();
            case ActivationFunctions.sigmoidFunction:
                return super().getSigmoid();
            case ActivationFunctions.tanhFunction:
                return super().getTanh();
            case ActivationFunctions.reLUFunction:
                return super().getreLU();
            case ActivationFunctions.leakyreLUFunction:
                return super().getLeakyreLU();
            
class TrainHandler (object):
    def __init__(self,
                 trainRule:TrainRules=TrainRules.deltaRule):
        self.trainRule = trainRule;
        
    def getCorrection(self,
                      x:list,
                      w:list,
                      eta:float,
                      y:float,
                      yd:float) -> list:
        match self.trainRule:
            case TrainRules.deltaRule:
                return self.getDeltaRuleCorrection(x, w, eta, y, yd);
    
    def getDeltaRuleCorrection(self,
                               x:list,
                               w:list,
                               eta:float,
                               y:float,
                               yd:float) -> list:
        correction = [];
        for i in range(0, len(w), 1):
            correction.append(w[i] + eta * (yd - y) * x[i]);
            
        return correction;
    
def main():
    theta = 0.8417
    eta = 0.1
    yd0 = 1
    yd1 = 0

    w = [-0.5441, 0.5562, -0.4074]
    x0 = [-1,2,2]
    x1 = [-1,4,4]

    e = 1
    iteration = 0
    
    print("Perceptron Neural Network\n\nParameters:");
    print("\n\t * Wieghts: " + str(w) + 
          "\n\t * Set A:" + str(x0) + 
          "\n\t * Set B:" + str(x1) + 
          "\n\nTraining:\n");
    
    trainHandler = TrainHandler(trainRule=TrainRules.deltaRule);
        
    while e != 0:
        print("\tActual weight set: " + str(w));
        neuron = MCPNeuron(x=x0,
                           w=w,
                           theta=theta);
        
        tmpWieght = trainHandler.getCorrection(x=x0,
                                               w=w,
                                               eta=eta,
                                               y=neuron.getActivation(),
                                               yd=yd0);
        
        e0 = yd0 - neuron.getActivation();
        
        w = tmpWieght;
        
        neuron = MCPNeuron(x=x1,
                           w=w,
                           theta=theta);
        
        tmpWieght = trainHandler.getCorrection(x=x1,
                                               w=w,
                                               eta=eta,
                                               y=neuron.getActivation(),
                                               yd=yd1);
        
        e1 = yd1 - neuron.getActivation();
        
        w = tmpWieght;
        
        e = e0 - e1;
        
        print("\tIteraction (" + str(iteration) +"): (e(x0) = " + str(e0) + " ; e(x1) = " + str(e1) + ") | f(e) = " + str(e));
        print("\tNew weight set: " + str(w) + "\n\n");
        
        iteration += 1;
        
        time.sleep(1);
    
if __name__ == "__main__":
    main();