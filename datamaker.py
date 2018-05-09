#!/usr/bin/python
from datatype import *
import os
import shutil
import copy



class DataMaker:
    def __init__(self,Object,**option):
        self.startidx = option.get("startidx", 0)
        self.directory = option.get("directory", "input")
        self.name = option.get("name", "input")
        self.extension = option.get("extension", "in")
        self.assertion = option.get("assertion",[])
        self.Object=Object
        self.option=option

        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)

        os.mkdir(self.directory)



    def __call__(self,Object,**option):
        self.__init__(self,Object,**option)

    def create(self,dataset):
        for i,data in enumerate(dataset):
            f = open(self.directory + "/" + self.name + str(i + self.startidx) + '.' + self.extension, "w")
            objectData = self.Object(**data)
            f.write(str(objectData))

            for assertFunc in self.assertion:
                if not assertFunc(objectData):
                    print("warning : {}th dataset is fail of {} test".format(i, assertFunc.__name__))
            print("create {}th data".format(i))
            f.close()

class LinearDataMaker(DataMaker):
    def __init__(self,Object,testcase,**option):
        DataMaker.__init__(self,Object,**option)

        self.interval=option.get("interval",0)
        self.start=option.get("start",0)
        dataset=[]
        for i in range(testcase):
            option['range']=(self.start+self.interval*i,self.start+self.interval*(i+1)-1)
            dataset.append(copy.deepcopy(option))
        self.create(dataset)

class GroupDataMaker(DataMaker):
    def __init__(self,Object,group,**option):
        DataMaker.__init__(self, Object, **option)

        dataset=[]
        for g in group:
            for i in range(g['num']):
                dataset.append(g)
        self.create(dataset)
