import GraphTools;
import sys

class HeuristicSearch (object):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 destiny:str,
                 heuristic:dict):
        self.graph = graph;
        self.start = start;
        self.destiny = destiny;
        self.heuristic = heuristic;
        self.nodes = None;
        self.solution = [];

class GreedSearch (HeuristicSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 destiny:str,
                 heuristic:dict):
        super().__init__(graph,
                         start,
                         destiny,
                         heuristic);
        self.nodeList = [];
        self.foundDestiny = False;
        
    def search(self):
        self.nodes = {self.start:
                      GraphTools.HeuristicNode(self.start,
                                               GraphTools.NodeColor.gray,
                                               0,
                                               self.heuristic[self.start],
                                               self.heuristic[self.start],
                                               "NhR")};
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.HeuristicNode(node,
                                                            GraphTools.NodeColor.white,
                                                            sys.maxsize,
                                                            self.heuristic[node],
                                                            sys.maxsize,
                                                            "NhR")});
        
        self.nodeList = [self.nodes[self.start]];
        
        while (len(self.nodeList) > 0):
            self.nodeList = sorted(self.nodeList, key=lambda node: node.cost);
            currNode = self.nodeList[0];
            currNode.color = GraphTools.NodeColor.gray;
            
            if currNode.node == self.destiny:
                currNode.color = GraphTools.NodeColor.black;
                self.solution.append(currNode);
                break;
            
            self.nodeList = [];
            for node in self.graph.adjacenceList[currNode.node]:
                if self.nodes[node['node']].color == GraphTools.NodeColor.white:
                    self.nodes[node['node']].distance = node['dist'];
                    self.nodes[node['node']].cost = self.nodes[node['node']].heuristic;
                    self.nodes[node['node']].root = currNode.node;
                    self.nodeList.append(self.nodes[node['node']])
            
            currNode.color = GraphTools.NodeColor.black;
            self.solution.append(currNode);
        
        return self.solution;
    
class AStarSearch (HeuristicSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 destiny:str,
                 heuristic:dict):
        super().__init__(graph,
                         start,
                         destiny,
                         heuristic);
        self.nodeList = [];
        self.foundDestiny = False;
        
    def search(self):
        self.nodes = {self.start:
                      GraphTools.HeuristicNode(self.start,
                                               GraphTools.NodeColor.gray,
                                               0,
                                               self.heuristic[self.start],
                                               self.heuristic[self.start],
                                               "NhR")};
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.HeuristicNode(node,
                                                            GraphTools.NodeColor.white,
                                                            sys.maxsize,
                                                            self.heuristic[node],
                                                            sys.maxsize,
                                                            "NhR")});
        
        self.nodeList = [self.nodes[self.start]];
        
        while (len(self.nodeList) > 0):
            self.nodeList = sorted(self.nodeList, key=lambda node: node.cost);
            currNode = self.nodeList[0];
            currNode.color = GraphTools.NodeColor.gray;
            
            if currNode.node == self.destiny:
                currNode.color = GraphTools.NodeColor.black;
                self.solution.append(currNode);
                break;
            
            self.nodeList = [];
            for node in self.graph.adjacenceList[currNode.node]:
                if self.nodes[node['node']].color == GraphTools.NodeColor.white:
                    self.nodes[node['node']].distance = node['dist'];
                    self.nodes[node['node']].cost = self.nodes[node['node']].distance + self.nodes[node['node']].heuristic;
                    self.nodes[node['node']].root = currNode.node;
                    self.nodeList.append(self.nodes[node['node']])
            
            currNode.color = GraphTools.NodeColor.black;
            self.solution.append(currNode);
        
        return self.solution;

class IDAStarSearch (HeuristicSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 destiny:str,
                 heuristic:dict):
        super().__init__(graph,
                         start,
                         destiny,
                         heuristic);
        self.nodeList = [];
        self.foundDestiny = False;
        self.limit = 0;
        
    def search(self):
        while not self.foundDestiny:
            self.nodes = {self.start:
                      GraphTools.HeuristicNode(self.start,
                                               GraphTools.NodeColor.gray,
                                               0,
                                               self.heuristic[self.start],
                                               self.heuristic[self.start],
                                               "NhR")};
        
            for node in list(self.graph.adjacenceList.keys()):
                if node != self.start:
                    self.nodes.update({node:
                                    GraphTools.HeuristicNode(node,
                                                                GraphTools.NodeColor.white,
                                                                sys.maxsize,
                                                                self.heuristic[node],
                                                                sys.maxsize,
                                                                "NhR")});
                
            self.solution = [];
            self.nodeList = [self.nodes[self.start]];
            while (len(self.nodeList) > 0):
                self.nodeList = sorted(self.nodeList, key=lambda node: node.cost);
                currNode = self.nodeList[0];
                currNode.color = GraphTools.NodeColor.gray;
                
                if currNode.cost > self.limit:
                    self.limit = currNode.cost;
                    break;
                
                if currNode.node == self.destiny:
                    currNode.color = GraphTools.NodeColor.black;
                    self.solution.append(currNode);
                    self.foundDestiny = True;
                    break;
                
                self.nodeList = [];
                for node in self.graph.adjacenceList[currNode.node]:
                    if self.nodes[node['node']].color == GraphTools.NodeColor.white:
                        self.nodes[node['node']].distance = node['dist'];
                        self.nodes[node['node']].cost = self.nodes[node['node']].distance + self.nodes[node['node']].heuristic;
                        self.nodes[node['node']].root = currNode.node;
                        self.nodeList.append(self.nodes[node['node']])
                
                currNode.color = GraphTools.NodeColor.black;
                self.solution.append(currNode);
            
        return self.solution;

class RBFSearch (HeuristicSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 destiny:str,
                 heuristic:dict):
        super().__init__(graph,
                         start,
                         destiny,
                         heuristic);
        self.nodeList = [];
        self.foundDestiny = False;
        self.limit = 0;
        
    def expandNode(self):
        self.nodeList = sorted(self.nodeList, key=lambda node: node.cost);
        currNode = self.nodeList[0];
        
        if currNode.cost > self.limit:
            self.limit = self.nodeList[len(self.nodeList) - 1].cost;
            return;
        
        currNode.color = GraphTools.NodeColor.gray;
        if (currNode.node == self.destiny) and (not self.foundDestiny):
            self.foundDestiny = True;
            currNode.color = GraphTools.NodeColor.black;
            self.solution.append(currNode);
            return;
        
       
        self.nodeList = [];
        for node in self.graph.adjacenceList[currNode.node]:
            if self.nodes[node['node']].color == GraphTools.NodeColor.white:
                self.nodes[node['node']].distance = node['dist'];
                self.nodes[node['node']].cost = self.nodes[node['node']].distance + self.nodes[node['node']].heuristic;
                self.nodes[node['node']].root = currNode.node;
                self.nodeList.append(self.nodes[node['node']])
            
        self.expandNode();
        
        if self.foundDestiny:
           currNode.color = GraphTools.NodeColor.black;
           self.solution.append(currNode);
           return;
    
    def search(self):
        self.nodes = {self.start:
                      GraphTools.HeuristicNode(self.start,
                                               GraphTools.NodeColor.gray,
                                               0,
                                               self.heuristic[self.start],
                                               self.heuristic[self.start],
                                               "NhR")};
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.HeuristicNode(node,
                                                            GraphTools.NodeColor.white,
                                                            sys.maxsize,
                                                            self.heuristic[node],
                                                            sys.maxsize,
                                                            "NhR")});
        
        while not self.foundDestiny:
            self.nodeList = [self.nodes[self.start]];
            self.expandNode();
        
        self.solution.reverse();
        return self.solution;

class HillClimbingSearch (HeuristicSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 destiny:str,
                 heuristic:dict):
        super().__init__(graph,
                         start,
                         destiny,
                         heuristic);
        self.nodeList = [];
        self.foundDestiny = False;
    
        
    def search(self):
        self.nodes = {self.start:
                      GraphTools.HeuristicNode(self.start,
                                               GraphTools.NodeColor.gray,
                                               0,
                                               self.heuristic[self.start],
                                               self.heuristic[self.start],
                                               "NhR")};
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.HeuristicNode(node,
                                                            GraphTools.NodeColor.white,
                                                            sys.maxsize,
                                                            self.heuristic[node],
                                                            sys.maxsize,
                                                            "NhR")});
        
        self.nodeList = [self.nodes[self.start]];
        lastCost = self.heuristic[self.start];
        
        while (len(self.nodeList) > 0):
            self.nodeList = sorted(self.nodeList, key=lambda node: node.cost);
            currNode = [node for node in self.nodeList if node.cost <= lastCost][0];
            currNode.color = GraphTools.NodeColor.gray;
            lastCost = currNode.cost;
            
            if currNode.node == self.destiny:
                currNode.color = GraphTools.NodeColor.black;
                self.solution.append(currNode);
                break;
            
            self.nodeList = [];
            for node in self.graph.adjacenceList[currNode.node]:
                if self.nodes[node['node']].color == GraphTools.NodeColor.white:
                    self.nodes[node['node']].distance = node['dist'];
                    self.nodes[node['node']].cost = self.nodes[node['node']].heuristic;
                    self.nodes[node['node']].root = currNode.node;
                    self.nodeList.append(self.nodes[node['node']])
            
            currNode.color = GraphTools.NodeColor.black;
            self.solution.append(currNode);
        
        return self.solution;
          
def createGraph() -> GraphTools.Graph:
    graph = GraphTools.Graph();
    graph.addNode("v",
                  [{"node":"r","dist":6}]); 
    graph.addNode("r",
                  [{"node":"v","dist":6}, {"node":"s","dist":6}]);
    graph.addNode("s",
                  [{"node":"r","dist":6}, {"node":"w","dist":5}]);
    graph.addNode("w",
                  [{"node":"s","dist":5}, {"node":"t","dist":35}, {"node":"x","dist":7}]);
    graph.addNode("t",
                  [{"node":"w","dist":35}, {"node":"x","dist":25}, {"node":"u","dist":5}]);
    graph.addNode("x",
                  [{"node":"w","dist":7}, {"node":"t","dist":25}, {"node":"y","dist":9}]);
    graph.addNode("u",
                  [{"node":"t","dist":5} ,{"node":"y","dist":7}]);
    graph.addNode("y",
                  [{"node":"x","dist":9} ,{"node":"u","dist":7}]);
    
    return graph

def createHeuristicA() -> dict:
    return {"s":36,
            "w":33,
            "x":24,
            "t":0,
            "u":3,
            "y":12,
            "r":42,
            "v":50}
    
def createHeuristicB() -> dict:
    return {"s":36,
            "w":44,
            "x":24,
            "t":0,
            "u":3,
            "y":12,
            "r":42,
            "v":50}
      
def main():
    graph = createGraph();
    startNode = input("Please, set the desired start node from: ");
    searchAlgorithmChoose = int(input("Please, select the desired heuristic search algorithm:\n"+
                                      "\t1-Greed Search\n"+
                                      "\t2-A* Search\n"+
                                      "\t3-Iterative Deepening A* (IDA*) Search\n"+
                                      "\t4-Recursive Best-first (RBF) Search\n"+
                                      "\t5-Hill Climbing Search\n"));
    destinyNode = input("Please, set the desired destiny node: ");
    
    match searchAlgorithmChoose:
        case 1:
            heuristic = createHeuristicA();
            searchAlgorithm = GreedSearch(graph,
                                          startNode,
                                          destinyNode,
                                          heuristic)
            solution = searchAlgorithm.search();
        case 2:
            heuristic = createHeuristicA();
            searchAlgorithm = AStarSearch(graph,
                                          startNode,
                                          destinyNode,
                                          heuristic)
            solution = searchAlgorithm.search();
        case 3:
            heuristic = createHeuristicA();
            searchAlgorithm = IDAStarSearch(graph,
                                            startNode,
                                            destinyNode,
                                            heuristic)
            solution = searchAlgorithm.search();
        case 4:
            heuristic = createHeuristicB();
            searchAlgorithm = RBFSearch(graph,
                                        startNode,
                                        destinyNode,
                                        heuristic)
            solution = searchAlgorithm.search();
        case 5:
            heuristic = createHeuristicA();
            searchAlgorithm = HillClimbingSearch(graph,
                                                 startNode,
                                                 destinyNode,
                                                 heuristic)
            solution = searchAlgorithm.search();
        case _:
            print("Invalid version!");
        
    for step in list(solution):
        print("The cost (g_n|f_n|h_n) between " + step.root + " and " + step.node + " is " + str(step.distance) + "|"
                                                                                           + str(step.cost) + "|" 
                                                                                           + str(step.heuristic));
        
    print("\n\nEnd of heuristic search algorithm simulation!")
    
if __name__ == "__main__":
    main();