import numpy as np

with open('graf.txt', 'r') as myfile:
    content = myfile.readlines()

content = [x.strip() for x in content]
content = [x.replace(" ", "") for x in content]
content = [x.split(';') for x in content]
content = [[int(j) for j in i] for i in content]

class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight

    def __repr__(self):
        return str(self.start) + ";" + str(self.end) + ";" + str(self.weight)

class Graph:
    def __init__(self):
        self.adj = {} #Adjacency matrix that holds graph data
        self.vertexCount = 0

    def addVertex(self, vertex):
        if vertex in self.adj:
            return "Vertex already exists"
        #if vertex != self.vertexCount:
        #    return "Don't skip a vertex"
        self.adj[vertex] = []
        self.vertexCount += 1

    def addEdge(self, start, end, weight):
        if start not in self.adj:
            return "Starting vertex not in graph"
        if end not in self.adj:
            return "Ending vertex not in graph"
        if start == end:
            return "Cannot have same start and end vertex"
        edge = Edge(start, end, weight)
        self.adj[start].append(edge)

    def doesEdgeExist(self, start, end):
        for vertex in self.adj:
            for edge in self.adj[vertex]:
                if edge.start == start and edge.end == end:
                    return (True, edge)
        return (False, None)

    def floydwarshall(self):
        M = [[9999 for x in range(len(self.adj))] for y in range(len(self.adj))]
        poprzednik = [[-1 for x in range(len(self.adj))] for y in range(len(self.adj))]
        for x in range(len(M)):
            for y in range(len(M[0])):
                if x == y:
                    M[x][y] = 0
                exists, edge = self.doesEdgeExist(x, y)
                if exists:
                    M[x][y] = edge.weight
                    poprzednik[x][y] = x

        for k in range(len(M)):
            for i in range(len(M)):
                for j in range(len(M)):
                    newDistance = M[i][k] + M[k][j]
                    if newDistance < M[i][j]:
                        M[i][j] = newDistance
                        poprzednik[i][j] = poprzednik[k][j]
        return (M, poprzednik)

gr = Graph()
#print(content)
for i in content:
    gr.addVertex(i[0])
    gr.addVertex(i[1])
    gr.addEdge(i[0],i[1],i[2])
    #print(i[0])

M, poprz = gr.floydwarshall()

for i in range(len(M)):
    print(*M[i], sep='\t')

for i in range(len(poprz)):
    print(*poprz[i], sep='\t')
