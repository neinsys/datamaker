#!/usr/bin/python
from datatype import *
import os
import shutil



class DataMaker:
    def __init__(self,Object,**option):
        self.startidx = option.get("startidx", 0)
        self.directory = option.get("directory", "input")
        self.name = option.get("name", "input")
        self.extension = option.get("extension", "in")
        self.Object=Object
        self.option=option

        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)

        os.mkdir(self.directory)



    def __call__(self,Object,**option):
        self.__init__(self,Object,**option)

    def create(self,dataset):
        for i in range(len(dataset)):
            f = open(self.directory + "/" + self.name + str(i + self.startidx) + '.' + self.extension, "w")
            f.write(str(self.Object(dataset[i][0], dataset[i][1],**dataset[i][2])))
            print dataset[i][0],dataset[i][1]
            f.close()

class LinearDataMaker(DataMaker):
    def __init__(self,Object,testcase,**option):
        DataMaker.__init__(self,Object,**option)

        self.interval=option.get("interval",0)
        self.start=option.get("start",0)
        dataset=[]
        for i in range(testcase):
            dataset.append([self.start+self.interval*i,self.start+self.interval*(i+1)-1,option])
        self.create(dataset)

class GroupDataMaker(DataMaker):
    def __init__(self,Object,group,**option):
        DataMaker.__init__(self, Object, **option)

        dataset=[]
        for g in group:
            low=g['nlow']
            high=g['nhigh']
            num=g['num']
            for i in range(num):
                dataset.append([low,high,g])
        self.create(dataset)
