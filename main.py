
from DM import *
from assertion import *


class FlowGraph(Graph):
    def __init__(self,Range, **option):
        Graph.__init__(self,Range,**option)
        self.supplyNodeRange = option.get("supplyRange",[0,self.vertex])
        self.demandNodeRange = option.get("demandRange",[0,self.vertex])
        self.disjointNode = option.get("disjointNode",True)

        self.supplyNode = randint(self.supplyNodeRange[0],self.supplyNodeRange[1])
        self.demandNode = randint(self.demandNodeRange[0],self.demandNodeRange[1])
        if self.disjointNode:
            exceed = self.supplyNode + self.demandNode - self.vertex
            self.supplyNode -= (exceed + 1) // 2
            self.demandNode -= (exceed + 1) // 2
        self.supplyNodeElement = []
        self.demandNodeElement = []

    def create(self):
        Graph.create(self)

        contain = set()

        for i in range(self.supplyNode):
            supplyNodeIndex = randint(self.startVertex, self.startVertex + self.vertex - 1)
            supplyNodeWeight = randint(self.weightRange[0],self.weightRange[1])

            while supplyNodeIndex in contain:
                supplyNodeIndex = randint(self.startVertex, self.startVertex + self.vertex - 1)
            
            self.supplyNodeElement.append((supplyNodeIndex,supplyNodeWeight))

        if not self.disjointNode:
            contain = set()
        
        for i in range(self.demandNode):
            demandNodeIndex = randint(self.startVertex, self.startVertex + self.vertex - 1)
            demandNodeWeight = randint(self.weightRange[0],self.weightRange[1])

            while demandNodeIndex in contain:
                demandNodeIndex = randint(self.startVertex, self.startVertex + self.vertex - 1)
            
            self.demandNodeElement.append((demandNodeIndex,demandNodeWeight))
        return self

    def __str__(self):
        self.create()
        ret = f"p min {self.vertex} {self.edge}\n"
        for v, w in self.supplyNodeElement:
            ret += f"n {v} {w}\n"
        for v, w in self.demandNodeElement:
            ret += f"n {v} {-w}\n"

        for e in self.edgeElement:
            F = e.From
            T = e.To
            W = e.Weight
            C = e.Cost
            ret += F"a {F} {T} 0 {W} {C}\n"
        return ret
        

def main():

    group = [
        {
            'low': 1,
            'high': 10,
            'num': 5,
            'hasWeight': True,
            'hasCost': True,
            'Range' : [5,20],
            'weightRange':[1,1000],
            'costRange':[1,1000],
            'edgeRange':[10,100],
        },
        {
            'low': 1,
            'high': 10,
            'num': 5,
            'hasWeight': True,
            'hasCost': True,
            'Range' : [5,20],
            'weightRange':[1,1000],
            'costRange':[-1000,1000],
            'edgeRange':[10,100],
        }
    ]
    GDM(FlowGraph, group, extension='min',name='test')



if __name__=="__main__":
    main()









