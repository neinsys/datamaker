
from DM import *
from assertion import *
def main():

    group = [
        {
            'low': 1,
            'high': 10,
            'num': 5,
            'isConnected':True,
            "edgeHigh":1,
            'edgeLow':1,
            'isUndirect':True,
        },
        {
            'low': 10,
            'high': 100,
            'num': 5,
        }
    ]
    def aaa(data):
        return True
    GDM(Graph, group,test=[
        tree_assertion
    ])



if __name__=="__main__":
    main()









