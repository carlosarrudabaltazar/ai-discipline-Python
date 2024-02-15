import GraphTools;
import sys

class BreadthFirstSearch (object):
    def __init__(self,
                 graph:GraphTools.Graph,
                 start:str):
        self.graph = graph;
        self.start = start;
        self.nodes = None;
        self.queue = [];
        
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
        
def createGraph() -> GraphTools.Graph:
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
        
def main():
    path = None;
    graph = createGraph();
    startNode = input("Please, set the desired start node from [r,s,t,u,v,w,x,y]:\n");
    searchAlgorithmChoose = int(input("Please, select the desired blind search algorithm:\n\t1-Breadth First Search\n"));
    
    if searchAlgorithmChoose == 1:
        searchAlgorithm = BreadthFirstSearch(graph,
                                             startNode);
        distancies = searchAlgorithm.search();
    else:
        print("Invalid version!");
        
    for distance in list(distancies.values()):
        print("The node " + distance.node + " is " + str(distance.distance) + " edges away from node " + startNode);
        
    print("End of blind search algorithm simulation!")
    
if __name__ == "__main__":
    main();