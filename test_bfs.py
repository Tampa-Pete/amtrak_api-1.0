#playing around with graphs to find breath-first-search tree
import json

graph = {
    1:[2,3],
    2:[1,3],
    3:[1,2,4],
    4:[3]
}
#pretty print graph
#print(json.dumps(graph, indent=4) )

#create a class for tree nodes
class TreeNode:
    def __init__(self, data):
        self.parent = None
        self.data = data
        self.children = []
    
    def __str__(self):
        child_string = ""
        for c in self.children:
            child_string += ',' + c.__str__()
        return '["' + str(self.data) + '"' + child_string + ']'

    def add_child(self, child):
        cnode = TreeNode(child)
        self.children.append(cnode)

class ChildTreeNode(TreeNode):
    def __init__(self, data, parent = None):
        super(data)
        self.parent = parent
    
    def add_parent(self, parent):
        assert isinstance(parent, ChildTreeNode)
        self.parent = parent

    def add_child(self, child):
        cnode = ChildTreeNode(child)
        cnode.parent = self


def process (parent, child):    #parent needs its children
    x = TreeNode(child)
    parent.add_child(x)
    return x

#BFS on graph, knowing the parents
queue = []
#need to know the parents, so "visited" is now "seen"
seen = set()
root = TreeNode(1)  #change 1 to "start"

#enqueue root node
seen.add(1)  #change 1 to "start"
queue.append(root)

while queue:
    review = queue.pop(0)   #queue already has node datastructure

    #see the reviewer's neighbors
    neighbors = graph[review.data]  #returns list

    for n in neighbors:
        if n not in seen:
            seen.add(n)
            p = process(review, n)
            queue.append(p)

#print tree
print(root)

'''
seen = [node]
query = [node]
bfstree = [node]
while query is not None:
    for x in graph[query[0]]:
        if x in seen:
            continue
        query.append(x)
        print (f"append {x} to {query}")
        bfstree.append(x)
        seen.append(x)
    query.pop(0)
#then add 4 to 3
'''