from enum import Enum;

class NodeColor (Enum):
    white=1;
    gray=2;
    black=3;
    
class Node (object):
    def __init__(self,
                 node:str,
                 color:NodeColor,
                 distance:float,
                 root:str):
        self.node = node;
        self.color = color;
        self.distance = distance;
        self.root = root;

class HeuristicNode (Node):
    def __init__(self,
                 node:str,
                 color:NodeColor,
                 distance:float,
                 heuristic:float,
                 cost:float,
                 root:str):
        super().__init__(node,
                         color,
                         distance,
                         root);
        self.heuristic = heuristic;
        self.cost = cost;
        

class Graph (object):
    def __init__(self):
        self.adjacenceList = {};
    
    def addNode(self,
                root:str,
                leaves:list):
        self.adjacenceList.update({root:leaves});
        