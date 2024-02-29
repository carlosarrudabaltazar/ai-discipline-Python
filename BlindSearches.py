import GraphTools;
import sys

class BlindSearch (object):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str):
        self.graph = graph;
        self.start = start;
        self.nodes = None;
        self.queue = [];

class BreadthFirstSearch (BlindSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str):
        super().__init__(graph,
                         start);
        
    def search(self):
        currNode = "";
        
        self.nodes = {self.start:
                      GraphTools.Node(self.start,
                                      GraphTools.NodeColor.gray,
                                      0,
                                      "NhR")};
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.Node(node,
                                                   GraphTools.NodeColor.white,
                                                   sys.maxsize,
                                                   "NhR")});
        
        self.queue.append(self.start);
        
        while len(self.queue) > 0:
            currNode = self.queue.pop(0);
            adjacentNodes = self.graph.adjacenceList[currNode];
            
            for adjacentNode in adjacentNodes:
                if (self.nodes[adjacentNode].color == GraphTools.NodeColor.white):
                    self.nodes[adjacentNode].color = GraphTools.NodeColor.gray;
                    self.nodes[adjacentNode].distance = self.nodes[currNode].distance + 1;
                    self.nodes[adjacentNode].root = currNode;
                    self.queue.append(self.nodes[adjacentNode].node) 
            
            self.nodes[currNode].color = GraphTools.NodeColor.black;
            
        return self.nodes;
    
class InDepthSearch (BlindSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str):
        super().__init__(graph,
                         start);
        self.time = 0;
        
    def visitNode(self,
                  node:GraphTools.Node):
        node.color = GraphTools.NodeColor.gray;
        self.time += 1;
        node.distance = self.time;
        
        adjacentNodes = self.graph.adjacenceList[node.node];
        
        for adjacentNodeName in adjacentNodes:
            adjacentNode = self.nodes[adjacentNodeName];
            if adjacentNode.color == GraphTools.NodeColor.white:
                self.nodes[adjacentNodeName].root = node.node;
                self.visitNode(self.nodes[adjacentNodeName]);
                
        node.color = GraphTools.NodeColor.black;
        self.time += 1;
        node.distance = self.time;
        
        self.nodes[node.node] = node;
            
        
    def search(self) -> list:
        self.nodes = {self.start:
                      GraphTools.Node(self.start,
                                      GraphTools.NodeColor.gray,
                                      1,
                                      "NhR")};
        self.time += 1;
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.Node(node,
                                                   GraphTools.NodeColor.white,
                                                   sys.maxsize,
                                                   "NhR")});

        for node in list(self.nodes.values()):
            if node.color == GraphTools.NodeColor.white:
                self.visitNode(node);
            
        return self.nodes;

class IterativeInDepthSearch (BlindSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 destiny:str):
        super().__init__(graph,
                         start);
        self.destiny = destiny;
        self.time = 0;
        self.limit = 1;
        self.foundDestiny = False;
        
    def visitNode(self,
                  node:GraphTools.Node,
                  level:int):
        node.color = GraphTools.NodeColor.gray;
        self.time += 1;
        node.distance = self.time;
        
        adjacentNodes = self.graph.adjacenceList[node.node];
        
        for adjacentNodeName in adjacentNodes:
            if level < self.limit and self.foundDestiny == False:
                adjacentNode = self.nodes[adjacentNodeName];
                if adjacentNode.color == GraphTools.NodeColor.white:
                    self.nodes[adjacentNodeName].root = node.node;
                    self.visitNode(self.nodes[adjacentNodeName],
                                   level + 1);
            else:
                if node.node == self.destiny:
                    self.foundDestiny = True;
                else:
                    break;
                
        if self.foundDestiny:
            node.color = GraphTools.NodeColor.black;
            self.time += 1;
            node.distance = self.time;
        else:
            self.time += 1;
            node.distance = self.time;
            node.color = GraphTools.NodeColor.white;
        
        self.nodes[node.node] = node;
            
    def search(self) -> list:
        self.nodes = {self.start:
                      GraphTools.Node(self.start,
                                      GraphTools.NodeColor.gray,
                                      1,
                                      "NhR")};
        self.time += 1;
        level = 0;
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.Node(node,
                                                   GraphTools.NodeColor.white,
                                                   sys.maxsize,
                                                   "NhR")});

        for node in list(self.nodes.values()):
            if node.color == GraphTools.NodeColor.white or self.foundDestiny == False:
                self.visitNode(node, level + 1);
                self.limit += 1;
            else:
                break;
            
        return self.nodes;
    
class LimitedInDepthSearch (BlindSearch):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str,
                 limit:int):
        super().__init__(graph,
                         start);
        self.limit = limit;
        self.level = 0;
        self.time = 0;
        self.resultNodes = {};
        
    def visitNode(self,
                  node:GraphTools.Node):
        if self.level < self.limit:  
            node.color = GraphTools.NodeColor.gray;
            self.time += 1;
            self.level += 1;
            node.distance = self.time;
        
        adjacentNodes = self.graph.adjacenceList[node.node];
        
        for adjacentNodeName in adjacentNodes:
            if self.level < self.limit:
                adjacentNode = self.nodes[adjacentNodeName];
                if adjacentNode.color == GraphTools.NodeColor.white:
                    self.nodes[adjacentNodeName].root = node.node;
                    self.visitNode(self.nodes[adjacentNodeName]);

        if self.level < self.limit:        
            node.color = GraphTools.NodeColor.black;
            self.time += 1;
            node.distance = self.time;
            
            self.nodes[node.node] = node;
            
        
    def search(self) -> list:
        self.nodes = {self.start:
                      GraphTools.Node(self.start,
                                      GraphTools.NodeColor.gray,
                                      1,
                                      "NhR")};
        self.time += 1;
        
        for node in list(self.graph.adjacenceList.keys()):
            if node != self.start:
                self.nodes.update({node:
                                   GraphTools.Node(node,
                                                   GraphTools.NodeColor.white,
                                                   sys.maxsize,
                                                   "NhR")});

        for node in list(self.nodes.values()):
            if node.color == GraphTools.NodeColor.white:
                self.visitNode(node);
            
        return self.nodes;
      
def createGraphA() -> GraphTools.Graph:
    graph = GraphTools.Graph();
    graph.addNode("v",
                  ["r"]); 
    graph.addNode("r",
                  ["v" , "s"]);
    graph.addNode("s",
                  ["r" , "w"]);
    graph.addNode("w",
                  ["t" , "x"]);
    graph.addNode("t",
                  ["w" , "x" , "u"]);
    graph.addNode("x",
                  ["w" , "t" , "y"]);
    graph.addNode("u",
                  ["t" , "y"]);
    graph.addNode("y",
                  ["x" , "u"]);
    
    return graph

def createGraphB() -> GraphTools.Graph:
    graph = GraphTools.Graph();
    graph.addNode("a",
                  ["b", "d", "e"]); 
    graph.addNode("b",
                  ["c", "e"]);
    graph.addNode("c",
                  ["a"]);
    graph.addNode("d",
                  ["e", "h"]);
    graph.addNode("e",
                  ["c"]);
    graph.addNode("f",
                  ["d", "g", "h"]);
    graph.addNode("g",
                  ["e"]);
    graph.addNode("h",
                  ["e"]);
    
    return graph
        
def main():
    path = None;
    graphA = createGraphA();
    graphB = createGraphB();
    startNode = input("Please, set the desired start node from: ");
    searchAlgorithmChoose = int(input("Please, select the desired blind search algorithm:\n"+
                                      "\t1-Breadth First Search\n"+
                                      "\t2-In-depth Search\n"+
                                      "\t3-Limited In-depth Search\n"+
                                      "\t4-Iterative In-depth Search\n"));
    
    match searchAlgorithmChoose:
        case 1:
            searchAlgorithm = BreadthFirstSearch(graphA,
                                                 startNode);
            distancies = searchAlgorithm.search();
        case 2:
            searchAlgorithm = InDepthSearch(graphB,
                                            startNode);
            distancies = searchAlgorithm.search();
        case 3:
            limit = int(input("Please set the search limit: "));
            searchAlgorithm = LimitedInDepthSearch(graphB,
                                                   startNode,
                                                   limit);
            distancies = searchAlgorithm.search();
        case 4:
            destiny = input("Please set destiny node: ");
            searchAlgorithm = IterativeInDepthSearch(graphB,
                                                     startNode,
                                                     destiny);
            distancies = searchAlgorithm.search();
        case _:
            print("Invalid version!");
        
    for distance in list(distancies.values()):
        print("The node " + distance.node + " is " + str(distance.distance) + " edges away from node " + startNode);
        
    print("End of blind search algorithm simulation!")
    
if __name__ == "__main__":
    main();