from random import randint,uniform,shuffle
from otherdatastructure import Edge,DisjointSet,Point,QueryData
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

    def __init__(self, Range, **option):
        self.isSort = option.get("isSort", False)
        self.compare = option.get("compare", None)
        self.disjoint = option.get("disjoint", False)
        self.exclude = option.get("exclude", set())
        self.Range = Range
        self.length = randint(self.Range[0], self.Range[1])
        self.element=[]

        self.elementRange = option.get("elementRange", [0,100])

        self.delimiter=option.get("delimiter",' ')

    def create(self):
        contain = set()
        for i in Range(self.length):
            num = randint(self.elementRange[0], self.elementRange[1])
            while (num in contain and self.disjoint) or num in self.exclude:
                num = randint(self.elementRange[0], self.elementRange[1])
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
            ret += str(i) + self.delimiter
        return ret



class Graph(DataType):
    def __init__(self, Range, **option):
        self.disjoint = option.get("disjoint", True)
        self.hasSelfEdge = option.get("hasSelfEdge", False)
        self.isSort = option.get("isSort", False)

        self.hasWeight = option.get("hasWeight", False)
        self.hasCost = option.get("hasCost", False)

        self.weightRange = option.get("weightRange", [0,0])

        self.costRange = option.get("costRange", [0,0])

        self.isConnected = option.get("isConnected", False)
        self.isUndirected = option.get("isUndirected", False)
        self.startVertex = option.get("startVertex", 1)
        self.vertex = randint(Range[0], Range[1])
        self.edgeRange = option.get("edgeRange", [0,self.vertex * (self.vertex - 1)])
        if self.isConnected and self.edgeRange[0] < self.vertex - 1:
            self.edgeRange[0] = self.vertex - 1

        if self.isUndirected and self.edgeRange[0] > self.vertex * (self.vertex - 1) / 2 and self.disjoint:
            self.edgeRange[0] = self.vertex * (self.vertex - 1) / 2
        if self.isUndirected and self.edgeRange[1] > self.vertex * (self.vertex - 1) / 2 and self.disjoint:
            self.edgeRange[1] = self.vertex * (self.vertex - 1) / 2

        if not self.isUndirected and self.edgeRange[0] > self.vertex * (self.vertex - 1) and self.disjoint:
            self.edgeRange[0] = self.vertex * (self.vertex - 1)
        if not self.isUndirected and self.edgeRange[1] > self.vertex * (self.vertex - 1) and self.disjoint:
            self.edgeRange[1] = self.vertex * (self.vertex - 1)


        if self.edgeRange[0]>self.edgeRange[1]:
            self.edgeRange[1]=self.edgeRange[0]
        self.edge = randint(self.edgeRange[0], self.edgeRange[1])
        self.edgeElement = []

    def create(self):
        contain = set()

        disjointset = DisjointSet(self.vertex)

        for i in range(self.edge):
            F = randint(self.startVertex, self.startVertex + self.vertex - 1)
            T = randint(self.startVertex, self.startVertex + self.vertex - 1)
            W = randint(self.weightRange[0], self.weightRange[1])
            C = randint(self.costRange[0], self.costRange[1])

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
    def __init__(self, aRange, **option):
        Graph.__init__(self, [0,0], **option)
        self.eachIdx = option.get("eachIdx", False)
        self.oneway = option.get("oneway", False)
        self.same = option.get("same", False)

        self.aRange=aRange
        self.bRange=option.get("bRange",aRange)
        self.aVertex = randint(self.aRange[0], self.aRange[1])
        self.bVertex = randint(self.bRange[0], self.bRange[1])
        self.vertex = self.aVertex + self.bVertex
        self.edgeRange = option.get("edgeRange", [0,self.aVertex * self.bVertex * 2])
        if self.isConnected and self.edgeRange[0] < self.vertex - 1:
            self.edgeRange[0] = self.vertex - 1
        if self.isUndirected and self.edgeRange[1] > self.aVertex * self.bVertex and self.disjoint:
            self.edgeRange[1] = self.aVertex * self.bVertex
        self.edge = randint(self.edgeRange[0], self.edgeRange[1])
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
            W = randint(self.weightRange[0], self.weightRange[1])
            C = randint(self.costRange[0], self.costRange[1])
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
    def __init__(self,Range,**option):
        self.queryRange = Range
        self.query=randint(self.queryRange[0],self.queryRange[1])

        self.element=list()
        self.isSort=option.get("isSort",False)
        self.elementRange=option.get("elementRange",[0,100])
        self.yRange=option.get("yRange",self.elementRange)

    def create(self):
        for i in range(self.query):
            x=randint(self.elementRange[0],self.elementRange[1])
            y=randint(self.yRange[0],self.yRange[1])
            self.element.append(QueryData(x,y))

    def __str__(self):
        self.create()
        ret=""
        ret+=str(len(self.element))+'\n'
        for i in self.element:
            ret+=str(i)+'\n'
        return ret


class String(DataType):
    pass

class Coordinate(DataType):
    def __init__(self,Range,**option):
        self.pointRange = Range
        self.point=randint(self.pointRange[0],self.pointRange[1])

        self.element=list()
        self.isRealNumber=option.get("isRealNumber",False)
        self.floating=option.get("floating",3)
        self.hasY=option.get("hasY",True)
        self.hasZ=option.get("hasZ",False)
        self.elementRange=option.get("elementRange",[0,100])
        self.xRange=option.get("xRange",self.elementRange)
        self.yRange=option.get("yRange",self.elementRange)
        self.zRange=option.get("zRange",self.elementRange)
        self.disjoint=option.get("disjoint",True)

    def getRandPoint(self):
        if not self.isRealNumber:
            x = randint(self.xRange[0], self.xRange[1])
            y = randint(self.yRange[0], self.yRange[1])
            z = randint(self.zRange[0], self.zRange[1])
        else:
            x = round(uniform(self.xRange[0], self.xRange[1]), self.floating)
            y = round(uniform(self.yRange[0], self.yRange[1]), self.floating)
            z = round(uniform(self.zRange[0], self.zRange[1]), self.floating)
        if not self.hasY:
            y = 0
        if not self.hasZ:
            z = 0
        return Point(x,y,z)

    def create(self):
        contain=set()

        for i in range(self.point):
            p=self.getRandPoint()
            while p in contain and self.disjoint:
                p=self.getRandPoint()
            self.element.append(p)
            contain.add(p)

    def __str__(self):
        self.create()
        ret=""
        ret+=str(len(self.element))
        for i in self.element:
            ret+=str(i.x)
            if self.hasY:
                ret+=' '+i.y
            if self.hasZ:
                ret+=' '+i.z
            ret+='\n'
        return ret





class Grid(DataType):
    def __init__(self,Range,**option):
        self.rowRange = Range
        self.columnRange=option.get("columnRange",Range)

        self.row=randint(self.rowRange[0],self.rowRange[1])
        self.column=randint(self.columnRange[0],self.columnRange[1])
        self.same=option.get("same",True)
        if self.same:
            self.column=self.row
        self.element=list()
        self.lowercase=option.get("lowercase",False)
        self.uppercase=option.get("uppercase",False)
        self.number=option.get("number",False)
        self.numberRange=option.get("numberRange",[0,100])
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
            for num in range(self.numberRange[0],self.numberRange[1]+1):
                if not str(num) in self.exclude:
                    self.element.append(str(num))
                    if not str(num) in contain:
                        contain[str(num)]=0
                    contain[str(num)]+=1

        for ch in self.include:
            if type(ch) is TupleType:
                while contain[ch[0]]<ch[1] and not ch[0] in self.exclude:
                    if not ch[0] in contain:
                        contain[ch[0]] = 0
                    contain[ch[0]]+=1
                    self.element.append(ch[0])
            else:
                while (not ch in contain or contain[ch]<1) and not ch in self.exclude:
                    if not ch in contain:
                        contain[ch] = 0
                    contain[ch]+=1
                    self.element.append(str(ch))
        shuffle(self.element)
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
        ret+=str(self.row)
        if not self.same:
            ret+=' '+str(self.column)
        ret+='\n'
        for r in self.grid:
            for c in r:
                ret+=c+self.delimiter
            ret+='\n'
        return ret

class TestCase(DataType):
    objects=[]
    def __init__(self,Range,object,**option):
        self.testcase=option.get("testcase",1)
        for tc in Range(self.testcase):
            self.objects.append(object(Range,**option))

    def __str__(self):
        ret=str(self.testcase)+'\n'
        for o in self.object:
            if ret[-1]!='\n':
                ret+='\n'
            ret+=str(o)
        return ret
