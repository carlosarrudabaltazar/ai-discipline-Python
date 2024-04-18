import pandas as pd;
from NeuralNetworkTools import Neuron;
from NeuralNetworkTools import Train;
from NeuralNetworkTools import ActivationFunctions;
from NeuralNetworkTools import TrainRules;

def main():
    theta = 0.8417
    eta = 0.1

    data = pd.DataFrame({'bias': [-1,-1],
                         'x[0]' : [2,4],
                         'x[1]' : [2,4],
                         'y': [1,0]});
                         
    #data = pd.DataFrame({'bias': [-1,-1,-1,-1,-1,-1],
    #                     'x[0]' : [1,2,3,4,5,6],
    #                     'x[1]' : [1,2,3,4,5,6],
    #                     'y': [1,1,1,0,0,0]});

    w = [-0.5441, 0.5562, -0.4074]

    e = 1
    iteration = 0
    
    print("Perceptron Neural Network\n\nParameters:");
    print("\n * Wieghts: {}".format(w) + 
          "\n * Sample: \n\n{}".format(data) + 
          "\n\nTraining:\n");

    mcp = Neuron(theta=theta,
                 activationFunction=ActivationFunctions.stepFunction);

    train = Train(neuron=mcp,
                  trainSample=data,
                  w=w,
                  eta=eta,
                  acceptableError=0,
                  trainRule=TrainRules.deltaRule);

    knowledge = train.train(verbose=True);

    print("Trained weight set: {}".format(knowledge));


if __name__ == "__main__":
    main();