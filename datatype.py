from random import randint
from otherdatastructure import Edge,DisjointSet
import string
from types import *
class DataType:
    def __init__(self, low, high, **option):
        self.element = randint(low, high)


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
        self.length = randint(low, high)
        self.element=[]

        self.elementLow = option.get("elementLow", 0)
        self.elementHigh = option.get("elementHigh", 100)

    def create(self):
        contain = set()
        for i in range(self.length):
            num = randint(self.elementLow, self.elementHigh)
            while (num in contain and self.disjoint) or num in self.exclude:
                num = randint(self.elementLow, self.elementHigh)
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
        self.vertex = randint(low, high)
        self.edgeLow = option.get("edgeLow", 0)
        self.edgeHigh = option.get("edgeHigh", self.vertex * (self.vertex - 1))
        if self.isConnected and self.edgeLow < self.vertex - 1:
            self.edgeLow = self.vertex - 1
        if self.isUndirected and self.edgeHigh > self.vertex * (self.vertex - 1) / 2 and self.disjoint:
            self.edgeHigh = self.vertex * (self.vertex - 1) / 2

        self.edge = randint(self.edgeLow, self.edgeHigh)
        self.edgeElement = []

    def create(self):
        contain = set()

        disjointset = DisjointSet(self.vertex)

        for i in range(self.edge):
            F = randint(self.startVertex, self.startVertex + self.vertex - 1)
            T = randint(self.startVertex, self.startVertex + self.vertex - 1)
            W = randint(self.weightLow, self.weightHigh)
            C = randint(self.costLow, self.costHigh)

            while (F == T and not self.hasSelfEdge) or \
                    (self.disjoint and Edge(F, T) in contain) or \
                    (self.disjoint and self.isUndirected and Edge(T, F) in contain) or \
                    (self.isConnected and len(self.edgeElement) < self.vertex - 1 and disjointset.find(
                            F - self.startVertex) == disjointset.find(T - self.startVertex)):
                F = randint(self.startVertex, self.startVertex + self.vertex - 1)
                T = randint(self.startVertex, self.startVertex + self.vertex - 1)
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
        self.aVertex = randint(self.aLow, self.aHigh)
        self.bVertex = randint(self.bLow, self.bHigh)
        self.vertex = self.aVertex + self.bVertex
        self.edgeLow = option.get("edgeLow", 0)
        self.edgeHigh = option.get("edgeHigh", self.aVertex * self.bVertex * 2)
        if self.isConnected and self.edgeLow < self.vertex - 1:
            self.edgeLow = self.vertex - 1
        if self.isUndirected and self.edgeHigh > self.aVertex * self.bVertex and self.disjoint:
            self.edgeHigh = self.aVertex * self.bVertex
        self.edge = randint(self.edgeLow, self.edgeHigh)
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
            idx = randint(self.startVertex, self.startVertex + limit - 1)
            while idx in contain:
                idx = randint(self.startVertex, self.startVertex + limit - 1)
            self.A.append(idx)
            contain.add(idx)

        if self.eachIdx:
            limit = self.bVertex
            contain.clear()

        for i in range(self.bVertex):
            idx = randint(self.startVertex, self.startVertex + limit - 1)
            while idx in contain:
                idx = randint(self.startVertex, self.startVertex + limit - 1)
            self.B.append(idx)
            contain.add(idx)

        contain = set()

        disjointset = DisjointSet(self.vertex)

        for i in range(self.edge):
            F = self.A[randint(0, self.aVertex - 1)]
            T = self.B[randint(0, self.bVertex - 1)]
            W = randint(self.weightLow, self.weightHigh)
            C = randint(self.costLow, self.costHigh)
            flag = randint(0, 1)
            if self.oneway:
                flag = 0

            if flag == 1:
                F, T = T, F
            while (F == T and not self.hasSelfEdge and not self.eachIdx) or \
                    (self.disjoint and Edge(F, T) in contain) or \
                    (self.disjoint and self.isUndirected and Edge(T, F) in contain) or \
                    (self.isConnected and len(self.edgeElement) < self.vertex - 1 and disjointset.find(
                            F - self.startVertex) == disjointset.find(T - self.startVertex)):
                F = self.A[randint(0, self.aVertex - 1)]
                T = self.B[randint(0, self.bVertex - 1)]
                flag = randint(0, 1)
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


class Query(DataType):
    pass

class String(DataType):
    pass

class Coordinate(DataType):
    pass

class Grid(DataType):
    def __init__(self,low,high,**option):
        self.rowLow=low
        self.rowHigh=high
        self.columnLow=option.get("columnLow",low)
        self.columnHigh=option.get("columnHigh",high)

        self.row=randint(self.rowLow,self.rowHigh)
        self.column=randint(self.columnLow,self.columnHigh)

        self.element=list()
        self.lowercase=option.get("lowercase",False)
        self.uppercase=option.get("uppercase",False)
        self.number=option.get("number",False)
        self.numberLow=option.get("numberLow",0)
        self.numberHigh=option.get("numberHigh",100)
        self.include=option.get("include",[])
        self.exclude=option.get("exclude",set())
        self.unique=option.get("unique",set())
        self.atLeastOne=option.get("atLeastOne",set())
        self.delimiter=option.get("delimiter",' ')


        contain={}
        if self.lowercase:
            for ch in string.ascii_lowercase:
                if not ch in self.exclude:
                    self.element.append(ch)
                    if not ch in contain:
                        contain[ch]=0
                    contain[ch] += 1

        if self.uppercase:
            for ch in string.ascii_uppercase:
                if not ch in self.exclude:
                    self.element.append(ch)
                    if not ch in contain:
                        contain[ch]=0
                    contain[ch] += 1

        if self.number:
            for num in range(self.numberLow,self.columnHigh+1):
                if not str(num) in self.exclude:
                    self.element.append(str(num))
                    if not ch in contain:
                        contain[ch]=0
                    contain[str(num)]+=1

        for ch in self.include:
            if type(ch) is TupleType:
                while contain[ch[0]]<ch[1] and not ch[0] in self.exclude:
                    if not ch[0] in contain:
                        contain[ch[0]] = 0
                    contain[ch[0]]+=1
                    self.element.append(ch[0])
            else:
                while contain[ch]<1 and not ch in self.exclude:
                    if not ch in contain:
                        contain[ch] = 0
                    contain[ch]+=1
                    self.element.append(ch)

        self.grid=[["" for i in range(self.column)] for j in range(self.row)]




    def create(self):
        contain=set()

        for ch in self.atLeastOne:
            r=randint(0,self.row)
            c=randint(0,self.column)
            if self.grid[r][c]!="":
                r = randint(0, self.row)
                c = randint(0, self.column)
            self.grid[r][c]=ch
            contain.add(ch)

        n=len(self.element)
        for r in range(self.row):
            for c in range(self.column):
                if self.grid[r][c]!="":
                    continue

                ch=self.element[randint(0,n-1)]
                while ch in contain and ch in self.unique:
                    ch=self.element[randint(0,n-1)]

                self.grid[r][c]=ch

    def __str__(self):
        self.create()
        ret=""
        ret+=str(self.row)+" "+str(self.column)+'\n'
        for r in self.grid:
            for c in r:
                ret+=c+self.delimiter
            ret+='\n'
        return ret

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