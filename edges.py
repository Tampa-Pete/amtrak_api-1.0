#Edges class for undirected graph

import logging

class edges:
    def __init__(self,e):
        self.logging()
        assert isinstance(e,list) and isinstance(e[1],tuple)
        self.edges = []
        for i in e:
            logging.debug(f"adding {i} to self")
            self.add_edge(i)
    def logging(self):
        if logging.getLogger().hasHandlers():
            logging.getLogger()
        else:
            logging.basicConfig(filename='edges.log', level=logging.INFO)
    def add_edge(self,i):
        if not self.exists(i):
            self.edges.append(i)
        else:
            logging.warning('edge (%s,%s) conflicts' % i[0], i[1])
    def exists(self,i):
        for j in self.edges:
            return i[0] == j[0] and i[1] == j[1]/
                or i[0] == j[1] and i[1] == j[0]
    def export(self):
        return self.edges
    def verify(self):
        for i in self.edges:
            pass
        #verify nodes are in order
        #verify edges are unduplicated
##
‘’’
edges consist of a unduplicated list of tuple pairs; these are the nodes which an edge connects.
nodes are ordered (if possible) ascending.
‘’’