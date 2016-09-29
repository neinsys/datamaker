
class Edge:
    def __init__(self, From, To, Weight=0, Cost=0):
        self.From = From
        self.To = To
        self.Weight = Weight
        self.Cost = Cost

    def __eq__(self, other):
        return getattr(other, 'From', None) == self.From and getattr(other, 'To', None) == self.To

    def __hash__(self):
        return hash(str(self.From) + str(self.To))


class DisjointSet:
    def __init__(self, N):
        self.tree = [0] * (N + 1)
        self.h = [0] * (N + 1)

    def find(self, idx):
        if self.tree[idx] == 0:
            return idx
        self.tree[idx] = self.find(self.tree[idx])
        return self.tree[idx]

    def union(self, A, B):
        A = self.find(A)
        B = self.find(B)
        if A == B:
            return
        if self.h[A] == self.h[B]:
            self.tree[B] = A
            self.h[A] += 1
        elif self.h[A] > self.h[B]:
            self.tree[B] = A
        else:
            self.tree[A] = B


class Point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def __eq__(self, other):
        return getattr(other,'x')==self.x and getattr(other,'y')==self.y and getattr(other,'z')==self.z

    def __hash__(self):
        return hash(str(self.x)+str(self.y)+str(self.z))


class QueryData:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        return getattr(other,'x')==self.x and getattr(other,'y')==self.y

    def __hash__(self):
        return hash(str(self.x)+str(self.y))

    def __str__(self):
        return str(self.x)+' '+str(self.y)
