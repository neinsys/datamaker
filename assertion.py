from otherdatastructure import DisjointSet



def tree_assertion(data):
    if len(data.edgeElement) != data.vertex-1:
        return False
    disjointset = DisjointSet(data.vertex)
    for e in data.edgeElement:
        F=e.From-data.startVertex
        T=e.To-data.startVertex
        if disjointset.find(F) == disjointset.find(T):
            return False
        disjointset.union(F,T)
    return True