from FuzzyLogic import MeaningFunction;
from FuzzyLogic import FuzzyHandler;
from FuzzyLogic import FuzzyOperation;
from FuzzyLogic import FuzzyMeaningFunction;

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