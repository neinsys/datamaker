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
            f.write(str(self.Object(**dataset[i])))
            print dataset[i]['low'],dataset[i]['high']
            f.close()

class LinearDataMaker(DataMaker):
    def __init__(self,Object,testcase,**option):
        DataMaker.__init__(self,Object,**option)

        self.interval=option.get("interval",0)
        self.start=option.get("start",0)
        dataset=[]
        for i in range(testcase):
            option['low']=self.start+self.interval*i
            option['high']=self.start+self.interval*(i+1)-1
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
