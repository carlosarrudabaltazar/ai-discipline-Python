from FuzzyLogic import MeaningFunction;
from FuzzyLogic import FuzzyHandler;
from FuzzyLogic import FuzzyOperation;
from FuzzyLogic import FuzzyMeaningFunction;
from matplotlib import pyplot as plt;

def main():
    option = 'y';
    
    while option == 'y':
        foodScore = 0;
        serviceScore = 0;
        tipPercentage = 0;

        foodMeaningFunction = MeaningFunction(realScale=list(range(0, 11)),
                                            fuzzyScale=["bad","good","excelent"],
                                            function=FuzzyMeaningFunction.triangle);

        serviceMeaningFunction = MeaningFunction(realScale=list(range(0, 11)),
                                                fuzzyScale=["bad","good","excelent"],
                                                function=FuzzyMeaningFunction.triangle);
        
        tipMeaningFunction = MeaningFunction(realScale=list(range(0, 26)),
                                            fuzzyScale=["small","medium","large"],
                                            function=FuzzyMeaningFunction.triangle);
        
        ax1 = plt.subplot(311);
        ax1.set_title("Food Meaning Function");
        ax1.plot(foodMeaningFunction.getMeaningFunction()["bad"]);
        ax1.plot(foodMeaningFunction.getMeaningFunction()["good"]);
        ax1.plot(foodMeaningFunction.getMeaningFunction()["excelent"]);

        ax2 = plt.subplot(312);
        ax2.set_title("Service Meaning Function");
        ax2.plot(serviceMeaningFunction.getMeaningFunction()["bad"]);
        ax2.plot(serviceMeaningFunction.getMeaningFunction()["good"]);
        ax2.plot(serviceMeaningFunction.getMeaningFunction()["excelent"]);

        ax3 = plt.subplot(313);
        ax3.set_title("Tip Meaning Function");
        ax3.plot(tipMeaningFunction.getMeaningFunction()["small"]);
        ax3.plot(tipMeaningFunction.getMeaningFunction()["medium"]);
        ax3.plot(tipMeaningFunction.getMeaningFunction()["large"]);

        plt.show()
        
        fuzzyHandler = FuzzyHandler();
        
        print("Fuzzy Logic - Tip Problem");
        foodScore = int(input("\nPlease insert the food score (0 - 10): "));
        serviceScore = int(input("\nPlease insert the service score (0 - 10): "));
        
        fuzzyfiedFood = fuzzyHandler.fuzzify(foodMeaningFunction.getMeaningFunction(),
                                            foodScore);
        
        fuzzyfiedService = fuzzyHandler.fuzzify(serviceMeaningFunction.getMeaningFunction(),
                                                serviceScore);
        lambdaTip = {};
        
        if (fuzzyfiedFood["excelent"] != 0 or fuzzyfiedService["excelent"]):
            lambdaTip["large"] = fuzzyHandler.fuzzyLogicOperation(fuzzyfiedFood["excelent"],
                                                                FuzzyOperation.fuzzyOr,
                                                                fuzzyfiedService["excelent"]);
        else:
            lambdaTip["large"] = 0;
            
        if (fuzzyfiedService["good"] != 0):
            lambdaTip["medium"] = fuzzyfiedService["good"];
        else:
            lambdaTip["medium"] = 0;
            
        if (fuzzyfiedService["bad"] !=0 and fuzzyfiedFood["bad"] != 0):
            lambdaTip["small"] = fuzzyHandler.fuzzyLogicOperation(fuzzyfiedFood["bad"],
                                                                FuzzyOperation.fuzzyAnd,
                                                                fuzzyfiedService["bad"]);
        else:
            lambdaTip["small"] = 0;
        
        tipPercentage = fuzzyHandler.defuzzify(lambdaValues=lambdaTip,
                                            targetMeaningFunction=tipMeaningFunction.getMeaningFunction());   
        
        print("\nThe ideal tip is: " + str(tipPercentage) + "%.");
        option = input("\n Do you want calculate another tip (y/n)? ");
    

if __name__ == "__main__":
    main();