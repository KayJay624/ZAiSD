import numpy as np

with open('graf3.txt', 'r') as myfile:
    content = myfile.readlines()

content = [x.strip() for x in content]
content = [x.replace(" ", "") for x in content]
content = [x.split(';') for x in content]
content = [[float(j) for j in i] for i in content]

class Vertex:
    def __init__(self, name, source=False, sink=False):
        self.name = name
        self.source = source
        self.sink = sink

class Edge:
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = 0
        self.returnEdge = None

    def getEnd():
        return self.end

    def __repr__(self):
        return str(self.start) + " -> " + str(self.end) # + " c:" + str(self.capacity)

class FlowNetwork:
    def __init__(self):
        self.vertices = []
        self.network = {}
        self.adj = {}

    def getSource(self):
        for vertex in self.vertices:
            if vertex.source == True:
                return vertex
        return None

    def getSink(self):
        for vertex in self.vertices:
            if vertex.sink == True:
                return vertex
        return None

    def setSource(self, name):
        for vertex in self.vertices:
            if name == vertex.name:
                vertex.source = True

    def setSink(self, name):
        for vertex in self.vertices:
            if name == vertex.name:
                vertex.sink = True;

    def getVertex(self, name):
        for vertex in self.vertices:
            if name == vertex.name:
                return vertex

    def vertexInNetwork(self, name):
        for vertex in self.vertices:
            if vertex.name == name:
                return True
        return False

    def addVertex(self, name, source=False, sink=False):
        if self.vertexInNetwork(name):
            #print(name)
            return 0
        newVertex = Vertex(name, source, sink)
        self.vertices.append(newVertex)
        self.network[newVertex.name] = []
        self.adj[newVertex.name] = []

    def addEdge(self, start, end, capacity):
        newEdge = Edge(start, end, capacity)
        returnEdge = Edge(end, start, 0)
        newEdge.returnEdge = returnEdge
        returnEdge.returnEdge = newEdge
        vertex = self.getVertex(start)
        self.network[vertex.name].append(newEdge)
        returnVertex = self.getVertex(end)
        self.network[returnVertex.name].append(returnEdge)
        self.adj[start].append(end)

    def bfs(self, start, end):
        queue = []
        visited = []
        visited.append(start)
        queue.append([(Edge(start, start, 0), 0)])
        while queue:
            path = queue.pop(0)
            node = path[-1][0].end
            if node == end:
                path.pop(0)
                return path

            for edge in self.network[node]:
                residualCapacity = edge.capacity - edge.flow
                #print(not (edge, residualCapacity) in path)
                
                if residualCapacity > 0 and not edge.end in visited:
                    new_path = list(path)
                    new_path.append((edge, residualCapacity))
                    #print(node)
                    queue.append(new_path)
                    visited.append(edge.end)
        return None

    def calculateMaxFlow(self):
        source = self.getSource()
        sink = self.getSink()
        #print(source.name)
        #print(sink.name)

        path = self.bfs(source.name, sink.name)
        while path != None:
            flow = min(edge[1] for edge in path)
            for edge, res in path:
                edge.flow += flow
                edge.returnEdge.flow -= flow
            path = self.bfs(source.name, sink.name)
            #print(path)
        return sum(edge.flow for edge in self.network[source.name])

def populate():
    fn = FlowNetwork()
    for i in content:
        fn.addVertex(i[0])
        fn.addVertex(i[1])
        fn.addEdge(i[0],i[1],i[2])

    # fn.addVertex('s')
    # fn.addVertex('c')
    # fn.addVertex('d')
    # # fn.addVertex('e')
    # fn.addVertex('t')
    # fn.addVertex('a')
    # fn.addVertex('b')
    # fn.addEdge('s', 'a', 4)
    # fn.addEdge('a', 'b', 4)
    # fn.addEdge('b', 't', 2)
    # fn.addEdge('s', 'c', 3)
    # fn.addEdge('c', 'd', 6)
    # fn.addEdge('d', 't', 6)
    # fn.addEdge('b', 'c', 3)
    #
    fn.setSource(43)
    return fn

############################################
fn = populate()
fn.setSink(180)
print("Max flow 43 - 180: ", fn.calculateMaxFlow())
#[print(k,v) for k,v in fn.network.items()]
############################################
result = []
fn = populate()
for v in fn.vertices:
    if v.name != 43:
        fn = populate()
        fn.setSink(v.name)
        maxFlow = fn.calculateMaxFlow()
        print("43 -",v.name, "maxFlow: ",maxFlow)
        result.append((v.name, maxFlow))

#print(result)
from operator import itemgetter
a = max(result,key=lambda x:x[1])
print("Max flow: " + str(a))

#print(fn.bfs(1,20))
