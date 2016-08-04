#!/usr/bin/python
from random import randint
import os
import shutil
class DataType:
    def rand(self,low,high):
        return randint(low,high)

    def create(self):
        return self

class Sequence(DataType):
    element=[]
    def __init__(self,low,high,**option):
        self.isSort=option.get("isSort",False)
        self.compare=option.get("compare",None)
        self.disjoint=option.get("disjoint",False)
        self.exclude=option.get("exclude",set())
        self.low=low
        self.high=high
        self.length=self.rand(low,high)

        self.elementLow=option.get("elementLow",0)
        self.elementHigh=option.get("elementHigh",100)



    def create(self):
        contain=set()
        for i in range(self.length):
            num=self.rand(self.elementLow,self.elementHigh)
            while (num in contain and self.disjoint) or num in self.exclude:
                num=self.rand(self.elementLow,self.elementHigh)
            self.element.append(num)
            contain.add(num)

        if self.isSort:
            self.element.sort(cmp=self.compare)
        return self


class Edge:
    def __init__(self, From, To,Weight=0,Cost=0):
        self.From = From
        self.To = To
        self.Weight=Weight
        self.Cost=Cost

    def __eq__(self, other):
        return getattr(other, 'From', None) == self.From and getattr(other, 'To', None) == self.To

    def __hash__(self):
        return hash(str(self.From) + str(self.To))

class DisjointSet:
    def __init__(self,N):
        self.tree=[0]*(N+1)
        self.h=[0]*(N+1)

    def find(self,idx):
        if self.tree[idx]==0:
            return idx
        self.tree[idx]=self.find(self.tree[idx])
        return self.tree[idx]

    def union(self,A,B):
        A=self.find(A)
        B=self.find(B)
        if A==B:
            return
        if self.h[A]==self.h[B]:
            self.tree[B]=A
            self.h[A]+=1
        elif self.h[A]>self.h[B]:
            self.tree[B]=A
        else:
            self.tree[A]=B



class Graph(DataType):

    def __init__(self,low,high,**option):
        self.disjoint=option.get("disjoint",True)
        self.hasSelfEdge=option.get("hasSelfEdge",False)
        self.isSort=option.get("isSort",False)

        self.hasWeight=option.get("hasWeight",False)
        self.hasCost=option.get("hasCost",False)

        self.weightLow=option.get("weightLow",0)
        self.weightHigh=option.get("weightHigh",0)

        self.costLow=option.get("costLow",0)
        self.costHigh=option.get("costHigh",0)

        self.isConnected=option.get("isConnected",False)
        self.isUndirected=option.get("isUndirected",False)
        self.startVertex=option.get("startVertex",1)
        self.vertex=self.rand(low,high)
        self.edgeLow=option.get("edgeLow",0)
        self.edgeHigh=option.get("edgeHigh",self.vertex*(self.vertex-1))
        if self.isConnected and self.edgeLow<self.vertex-1:
            self.edgeLow=self.vertex-1
        if self.isUndirected and self.edgeHigh>self.vertex*(self.vertex-1)/2 and self.disjoint:
            self.edgeHigh=self.vertex*(self.vertex-1)/2

        self.edge=self.rand(self.edgeLow,self.edgeHigh)
        self.edgeElement=[]



    def create(self):
        contain=set()

        disjointset = DisjointSet(self.vertex)

        for i in range(self.edge):
            F=self.rand(self.startVertex,self.startVertex+self.vertex-1)
            T=self.rand(self.startVertex,self.startVertex+self.vertex-1)
            W=self.rand(self.weightLow,self.weightHigh)
            C=self.rand(self.costLow,self.costHigh)


            while (F==T and not self.hasSelfEdge) or\
                    (self.disjoint and Edge(F,T) in contain) or\
                    (self.disjoint and self.isUndirected and Edge(T,F) in contain) or\
                    (self.isConnected and len(self.edgeElement)<self.vertex-1 and disjointset.find(F-self.startVertex)==disjointset.find(T-self.startVertex)):
                F = self.rand(self.startVertex, self.startVertex + self.vertex - 1)
                T = self.rand(self.startVertex, self.startVertex + self.vertex - 1)
            if self.isSort and F>T:
                F,T=T,F
            self.edgeElement.append(Edge(F,T,W,C))
            disjointset.union(F-self.startVertex,T-self.startVertex)
            contain.add(Edge(F,T))
        return self


class BipartiteGraph(Graph):


    A=[]
    B=[]
    def __init__(self,aLow,aHigh,bLow,bHigh,**option):
        Graph.__init__(self,0,0,**option)
        self.eachIdx=option.get("eachIdx",False)
        self.oneway=option.get("oneway",False)
        self.same=option.get("same",False)
        
        self.aVertex=self.rand(aLow,aHigh)
        self.bVertex=self.rand(bLow,bHigh)
        self.vertex=self.aVertex+self.bVertex
        self.edgeLow = option.get("edgeLow", 0)
        self.edgeHigh = option.get("edgeHigh", self.aVertex * self.bVertex *2)
        if self.isConnected and self.edgeLow < self.vertex - 1:
            self.edgeLow = self.vertex - 1
        if self.isUndirected and self.edgeHigh > self.aVertex * self.bVertex and self.disjoint:
            self.edgeHigh = self.aVertex * self.bVertex
        self.edge = self.rand(self.edgeLow, self.edgeHigh)

    def create(self):
        if self.same:
            self.bVertex=self.aVertex

        limit=self.aVertex+self.bVertex
        if self.eachIdx:
            limit=self.aVertex

        contain=set()
        for i in range(self.aVertex):
            idx=self.rand(self.startVertex,self.startVertex+limit-1)
            while idx in contain:
                idx=self.rand(self.startVertex,self.startVertex+limit-1)
            self.A.append(idx)
            contain.add(idx)

        if self.eachIdx:
            limit=self.bVertex
            contain.clear()

        for i in range(self.bVertex):
            idx=self.rand(self.startVertex,self.startVertex+limit-1)
            while idx in contain:
                idx=self.rand(self.startVertex,self.startVertex+limit-1)
            self.B.append(idx)
            contain.add(idx)

        contain = set()

        disjointset = DisjointSet(self.vertex)



        for i in range(self.edge):
            F = self.A[self.rand(0, self.aVertex-1)]
            T = self.B[self.rand(0, self.bVertex-1)]
            W = self.rand(self.weightLow, self.weightHigh)
            C = self.rand(self.costLow, self.costHigh)
            flag=self.rand(0,1)
            if self.oneway:
                flag=0

            if flag==1:
                F, T = T, F
            while (F == T and not self.hasSelfEdge and not self.eachIdx) or \
                    (self.disjoint and Edge(F, T) in contain) or \
                    (self.disjoint and self.isUndirected and Edge(T, F) in contain) or \
                    (self.isConnected and len(self.edgeElement) < self.vertex - 1 and disjointset.find(
                        F-self.startVertex) == disjointset.find(T-self.startVertex)):
                F = self.A[self.rand(0, self.aVertex - 1)]
                T = self.B[self.rand(0, self.bVertex - 1)]
                flag = self.rand(0, 1)
                if self.oneway:
                    flag = 0

                if flag == 1:
                    F, T = T, F
            if self.isSort and F>T:
                F,T=T,F
            self.edgeElement.append(Edge(F, T, W, C))
            disjointset.union(F-self.startVertex, T-self.startVertex)
            contain.add(Edge(F,T))
        return self

        


def BasicSequenceSerialize(seq):
    ret=""
    element=getattr(seq,"element")
    ret+=str(len(getattr(seq,"element")))+'\n'
    for i in element:
        ret+=str(i)+' '
    return ret

def BasicGraphSerialize(graph):
    ret=""
    v=getattr(graph,"vertex")
    e=getattr(graph,"edge")
    hasWeight=getattr(graph,"hasWeight")
    hasCost=getattr(graph,"hasCost")
    ret+=str(v)+' '+str(e)+'\n'
    edgeElement=getattr(graph,"edgeElement")
    for i in edgeElement:
        F=getattr(i,"From")
        T=getattr(i,"To")
        W=getattr(i,"Weight")
        C=getattr(i,"Cost")
        ret+=str(F)+' '+str(T)
        if hasWeight:
            ret+=' '+str(W)
        if hasCost:
            ret+=' '+str(C)
        ret+='\n'
    return ret


class DataMaker:
    def __init__(self,serialize,Object,**option):
        self.startidx = option.get("startidx", 0)
        self.directory = option.get("directory", "input")
        self.name = option.get("name", "input")
        self.extension = option.get("extension", "in")
        self.serialize=serialize
        self.Object=Object
        self.option=option

        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)

        os.mkdir(self.directory)



    def __call__(self,serialize,Object,**option):
        self.__init__(self,serialize,Object,**option)

    def create(self,dataset):
        for i in range(len(dataset)):
            f = open(self.directory + "/" + self.name + str(i + self.startidx) + '.' + self.extension, "w")
            f.write(self.serialize(self.Object(dataset[i][0], dataset[i][1],**dataset[i][2]).create()))
            f.close()

class LinearDataMaker(DataMaker):
    def __init__(self,serialize,Object,testcase,**option):
        DataMaker.__init__(self,serialize,Object,**option)

        self.interval=option.get("interval",0)
        self.start=option.get("start",0)
        dataset=[]
        for i in range(testcase):
            dataset.append([self.start+self.interval*i,self.start+self.interval*(i+1),option])
        self.create(dataset)

class GroupDataMaker(DataMaker):
    def __init__(self,serialize,Object,group,**option):
        DataMaker.__init__(self, serialize, Object, **option)

        dataset=[]
        for g in group:
            low=g['nlow']
            high=g['nhigh']
            num=g['num']
            for i in range(num):
                dataset.append([low,high,g])
        self.create(dataset)

DT=DataType
S=Sequence
G=Graph
BG=BipartiteGraph
BSS=BasicSequenceSerialize
BGS=BasicGraphSerialize
DM=DataMaker
LDM=LinearDataMaker
GDM=GroupDataMaker


