from random import randint;
import time;

class VaccumCleaner (object):
    
    def __init__(self):
        self.actualPosition = None;
        self.actualSituation = None;
        self.action = None;
        
    
    def getAction(self,
                  actualPosition:str,
                  actualSituation:bool) -> str:
        self.actualPosition = actualPosition;
        self.actualSituation = actualSituation;
         
        if self.actualSituation:
            self.action = "clean";
        elif self.actualPosition == "A":
            self.action = "right";
        elif self.actualPosition == "B":
            self.action = "left";
        
        return self.action;
    
class Environment (object):
    name = None;
    actualSituation = None;
    
    def __init__(self,
                 name:str,
                 actualSituation:bool):
        self.name = name;
        self.actualSituation = actualSituation;
        
    def setSituation(self,
                     newSituation:bool):
        self.actualSituation = newSituation;
    
    def setRadomSituation(self,
                          seed:int):
        if seed < 1:
            self.actualSituation = False;
        else:
            self.actualSituation = True;
            
    def setRoom(self,
                name:str):
        self.name = name;
        
class VacuumCleanerMetric (object):
    def __init__(self):
        self.latestAction = None;
        self.metric = 0;
    
    def setLatestAction(self,
                        latestAction:str):
        self.latestAction = latestAction;
        
    def addCleanPoint(self):
        self.metric += 1;
    
    def notCleanPenalty(self):
        if (self.latestAction != "clean" and
            self.latestAction != None and
            self.latestAction != "" and
            self.metric > 0):
            self.metric -= 1;
        
def basicVacuumCleaner(iterationsQtd:int):
    environment = Environment("A",
                              True);
    vaccumCleaner = VaccumCleaner();
    currAction = None;
    
    for i in range(iterationsQtd):
        currAction = vaccumCleaner.getAction(environment.name,
                                             environment.actualSituation);
        
        print("Room = " + environment.name + " | Actual situation = " + str(environment.actualSituation) + " | Action = " + currAction);
        
        if (currAction == "left"):
            environment.setRoom("A");
        elif (currAction == "right"):
            environment.setRoom("B");
        else:
            environment.setSituation(False);
        
        environment.setRadomSituation(randint(-10,10));
        
        time.sleep(0.5);

def metricVacuumCleaner(iterationsQtd:int):
    environment = Environment("A",
                              True);
    vaccumCleaner = VaccumCleaner();
    metricManager = VacuumCleanerMetric();
    currAction = None;
    
    for i in range(iterationsQtd):
        currAction = vaccumCleaner.getAction(environment.name,
                                             environment.actualSituation);
        
        metricManager.setLatestAction(currAction);
                
        print("Room = " + environment.name + " | Actual situation = " + str(environment.actualSituation) + " | Action = " + currAction);
        
        if (currAction == "left"):
            environment.setRoom("A");
            metricManager.notCleanPenalty();
        elif (currAction == "right"):
            environment.setRoom("B");
            metricManager.notCleanPenalty();
        else:
            environment.setSituation(False);
            metricManager.addCleanPoint();
            
        environment.setRadomSituation(randint(-10,10)); 
        
        time.sleep(0.5);  
    
    print("Vacuum cleaner agent's score: " + str(metricManager.metric));
    
def main():
    iterationsQtd = int(input("Please, set the desired number of iterations: "));
    vacuumCleanerVersion = input("What Vacuum Cleaner version do you want (basic/metric)?\n");
    
    if vacuumCleanerVersion == "basic":
        basicVacuumCleaner(iterationsQtd);
    elif vacuumCleanerVersion == "metric":
        metricVacuumCleaner(iterationsQtd);
    else:
        print("Invalid version!");
        
    print("End of vacuum Cleaner problem simulation!")
    
if __name__ == "__main__":
    main();
