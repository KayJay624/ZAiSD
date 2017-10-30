import numpy as np

with open('graf.txt', 'r') as myfile:
    content = myfile.readlines()

content = [x.strip() for x in content]
content = [x.replace(" ", "") for x in content]
content = [x.split(';') for x in content]
content = [[int(j) for j in i] for i in content]

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


    def __repr__(self):
        return str(self.start) + " -> " + str(self.end) + " c:" + str(self.capacity)

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

    def getEdges(self):
        allEdges = []
        for vertex in self.network:
            for edge in self.network[vertex]:
                allEdges.append(edge)
        return allEdges

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
        self.adj[start].append(newEdge)

    def getPath(self, start, end, path):
        if start == end:
            return path
        for edge in self.network[start]:
            residualCapacity = edge.capacity - edge.flow
            if residualCapacity > 0 and not (edge, residualCapacity) in path:
                result = self.getPath(edge.end, end, path + [(edge, residualCapacity)])
                if result != None:
                    #print(result)
                    return result

    def calculateMaxFlow(self):
        source = self.getSource()
        sink = self.getSink()
        if source == None or sink == None:
            return "Network does not have source and sink"
        path = self.getPath(source.name, sink.name, [])
        #print(path)
        while path != None:
            flow = min(edge[1] for edge in path)
            for edge, res in path:
                edge.flow += flow
                edge.returnEdge.flow -= flow
            #[print("(" + p[0].start + "," +p[0].end + ") ") for p in path]
            #print("----------------")
            path = self.getPath(source.name, sink.name, [])
        return sum(edge.flow for edge in self.network[source.name])

# gr = FlowNetwork()
#print(content)
#
# for i in content:
#     gr.addVertex(i[0])
#     gr.addVertex(i[1])
#     gr.addEdge(i[0],i[1],i[2])
#     #print(i[0])
#
# [print(x.name) for x in gr.vertices]
def populate():
    fn = FlowNetwork()
    # for i in content:
    #     fn.addVertex(i[0])
    #     fn.addVertex(i[1])
    #     fn.addEdge(i[0],i[1],i[2])
    # fn.setSource(1)
    for i in content:
        fn.addVertex(i[0])
        fn.addVertex(i[1])
        fn.addEdge(i[0],i[1],i[2])
        #print(i[0])

    # fn.addVertex(1)
    # fn.addVertex(10)
    # fn.addVertex(2)
    # fn.addVertex(3)
    # fn.addVertex(4)
    # fn.addVertex(5)
    # fn.addVertex(6)
    # #fn.setSink(10)
    # fn.setSource(1)
    # fn.addEdge(1, 2, 4)
    # fn.addEdge(2, 3, 4)
    # fn.addEdge(3, 10, 2)
    # fn.addEdge(1, 4, 3)
    # fn.addEdge(4, 5, 6)
    # fn.addEdge(5, 10, 6)
    # fn.addEdge(3, 4, 3)
    # fn.addEdge(1, 6, 10)
    fn.setSource(1)
    print(fn.adj)
    return fn

res = []
# fn = populate()
# for v in fn.vertices:
#     if v.name != 109:
#         fn = populate()
#         fn.setSink(v.name)
#         mf = fn.calculateMaxFlow()
#         res.append((v.name, mf))


# print(res)
# from operator import itemgetter
# a = max(res,key=lambda x:x[1])
# print("Max flow: " + str(a))

fn = populate()
fn.setSink(20)

print(fn)
#print(fn.adj)
# [print(e.start + " -> " + e.end + " flow:" +
# str(e.flow) + " capacity: " + str(e.capacity)) for e in fn.getEdges()]
print(fn.calculateMaxFlow())
# [print(e.start + " -> " + e.end + " flow:" +
# str(e.flow) + " capacity: " + str(e.capacity)) for e in fn.getEdges()]
