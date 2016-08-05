from random import randint
from otherdatastructure import Edge,DisjointSet
class DataType:
    def __init__(self, low, high, **option):
        self.element = self.rand(low, high)

    def rand(self, low, high):
        return randint(low, high)

    def create(self):
        return self

    def __str__(self):
        self.create()
        ret = ""
        ret += str(self.element)
        return ret


class Sequence(DataType):

    def __init__(self, low, high, **option):
        self.isSort = option.get("isSort", False)
        self.compare = option.get("compare", None)
        self.disjoint = option.get("disjoint", False)
        self.exclude = option.get("exclude", set())
        self.low = low
        self.high = high
        self.length = self.rand(low, high)
        self.element=[]

        self.elementLow = option.get("elementLow", 0)
        self.elementHigh = option.get("elementHigh", 100)

    def create(self):
        contain = set()
        for i in range(self.length):
            num = self.rand(self.elementLow, self.elementHigh)
            while (num in contain and self.disjoint) or num in self.exclude:
                num = self.rand(self.elementLow, self.elementHigh)
            self.element.append(num)
            contain.add(num)

        if self.isSort:
            self.element.sort(cmp=self.compare)
        return self

    def __str__(self):
        self.create();
        ret = ""
        ret += str(len(self.element)) + "\n"
        for i in self.element:
            ret += str(i) + ' '
        return ret



class Graph(DataType):
    def __init__(self, low, high, **option):
        self.disjoint = option.get("disjoint", True)
        self.hasSelfEdge = option.get("hasSelfEdge", False)
        self.isSort = option.get("isSort", False)

        self.hasWeight = option.get("hasWeight", False)
        self.hasCost = option.get("hasCost", False)

        self.weightLow = option.get("weightLow", 0)
        self.weightHigh = option.get("weightHigh", 0)

        self.costLow = option.get("costLow", 0)
        self.costHigh = option.get("costHigh", 0)

        self.isConnected = option.get("isConnected", False)
        self.isUndirected = option.get("isUndirected", False)
        self.startVertex = option.get("startVertex", 1)
        self.vertex = self.rand(low, high)
        self.edgeLow = option.get("edgeLow", 0)
        self.edgeHigh = option.get("edgeHigh", self.vertex * (self.vertex - 1))
        if self.isConnected and self.edgeLow < self.vertex - 1:
            self.edgeLow = self.vertex - 1
        if self.isUndirected and self.edgeHigh > self.vertex * (self.vertex - 1) / 2 and self.disjoint:
            self.edgeHigh = self.vertex * (self.vertex - 1) / 2

        self.edge = self.rand(self.edgeLow, self.edgeHigh)
        self.edgeElement = []

    def create(self):
        contain = set()

        disjointset = DisjointSet(self.vertex)

        for i in range(self.edge):
            F = self.rand(self.startVertex, self.startVertex + self.vertex - 1)
            T = self.rand(self.startVertex, self.startVertex + self.vertex - 1)
            W = self.rand(self.weightLow, self.weightHigh)
            C = self.rand(self.costLow, self.costHigh)

            while (F == T and not self.hasSelfEdge) or \
                    (self.disjoint and Edge(F, T) in contain) or \
                    (self.disjoint and self.isUndirected and Edge(T, F) in contain) or \
                    (self.isConnected and len(self.edgeElement) < self.vertex - 1 and disjointset.find(
                            F - self.startVertex) == disjointset.find(T - self.startVertex)):
                F = self.rand(self.startVertex, self.startVertex + self.vertex - 1)
                T = self.rand(self.startVertex, self.startVertex + self.vertex - 1)
            if self.isSort and F > T:
                F, T = T, F
            self.edgeElement.append(Edge(F, T, W, C))
            disjointset.union(F - self.startVertex, T - self.startVertex)
            contain.add(Edge(F, T))
        return self

    def __str__(self):
        self.create()
        ret = ""
        ret += str(self.vertex) + ' ' + str(self.edge) + '\n'
        for i in self.edgeElement:
            F = i.From
            T = i.To
            W = i.Weight
            C = i.Cost
            ret += str(F) + ' ' + str(T)
            if self.hasWeight:
                ret += ' ' + str(W)
            if self.hasCost:
                ret += ' ' + str(C)
            ret += '\n'
        return ret


class BipartiteGraph(Graph):
    def __init__(self, aLow, aHigh, **option):
        Graph.__init__(self, 0, 0, **option)
        self.eachIdx = option.get("eachIdx", False)
        self.oneway = option.get("oneway", False)
        self.same = option.get("same", False)

        self.aLow=aLow
        self.aHigh=aHigh
        self.bLow=option.get("bLow",aLow)
        self.bHigh=option.get("bHigh",aHigh)
        self.aVertex = self.rand(self.aLow, self.aHigh)
        self.bVertex = self.rand(self.bLow, self.bHigh)
        self.vertex = self.aVertex + self.bVertex
        self.edgeLow = option.get("edgeLow", 0)
        self.edgeHigh = option.get("edgeHigh", self.aVertex * self.bVertex * 2)
        if self.isConnected and self.edgeLow < self.vertex - 1:
            self.edgeLow = self.vertex - 1
        if self.isUndirected and self.edgeHigh > self.aVertex * self.bVertex and self.disjoint:
            self.edgeHigh = self.aVertex * self.bVertex
        self.edge = self.rand(self.edgeLow, self.edgeHigh)
        self.A=[]
        self.B=[]

    def create(self):
        if self.same:
            self.bVertex = self.aVertex

        limit = self.aVertex + self.bVertex
        if self.eachIdx:
            limit = self.aVertex

        contain = set()
        for i in range(self.aVertex):
            idx = self.rand(self.startVertex, self.startVertex + limit - 1)
            while idx in contain:
                idx = self.rand(self.startVertex, self.startVertex + limit - 1)
            self.A.append(idx)
            contain.add(idx)

        if self.eachIdx:
            limit = self.bVertex
            contain.clear()

        for i in range(self.bVertex):
            idx = self.rand(self.startVertex, self.startVertex + limit - 1)
            while idx in contain:
                idx = self.rand(self.startVertex, self.startVertex + limit - 1)
            self.B.append(idx)
            contain.add(idx)

        contain = set()

        disjointset = DisjointSet(self.vertex)

        for i in range(self.edge):
            F = self.A[self.rand(0, self.aVertex - 1)]
            T = self.B[self.rand(0, self.bVertex - 1)]
            W = self.rand(self.weightLow, self.weightHigh)
            C = self.rand(self.costLow, self.costHigh)
            flag = self.rand(0, 1)
            if self.oneway:
                flag = 0

            if flag == 1:
                F, T = T, F
            while (F == T and not self.hasSelfEdge and not self.eachIdx) or \
                    (self.disjoint and Edge(F, T) in contain) or \
                    (self.disjoint and self.isUndirected and Edge(T, F) in contain) or \
                    (self.isConnected and len(self.edgeElement) < self.vertex - 1 and disjointset.find(
                            F - self.startVertex) == disjointset.find(T - self.startVertex)):
                F = self.A[self.rand(0, self.aVertex - 1)]
                T = self.B[self.rand(0, self.bVertex - 1)]
                flag = self.rand(0, 1)
                if self.oneway:
                    flag = 0

                if flag == 1:
                    F, T = T, F
            if self.isSort and F > T:
                F, T = T, F
            self.edgeElement.append(Edge(F, T, W, C))
            disjointset.union(F - self.startVertex, T - self.startVertex)
            contain.add(Edge(F, T))
        return self

class TestCase(DataType):
    objects=[]
    def __init__(self,low,high,object,**option):
        self.testcase=option.get("testcase",1)
        for tc in range(self.testcase):
            self.objects.append(object(low,high,**option))

    def __str__(self):
        ret=str(self.testcase)+'\n'
        for o in object:
            if ret[-1]!='\n':
                ret+='\n'
            ret+=str(o)
        return ret