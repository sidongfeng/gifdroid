import json
from collections import defaultdict
import itertools

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.all_paths = []

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def printAllPathsUtil(self, u, d, visited, path):
        visited[u]= True
        path.append(u)
        if u == d:
            self.all_paths.append(path.copy())
        else:
            for i in self.graph[u]:
                if visited[i]== False:
                    self.printAllPathsUtil(i, d, visited, path)	
        path.pop()
        visited[u]= False

    def printAllPaths(self, s, d):
        visited =[False]*(self.V)
        path = []
        self.printAllPathsUtil(s, d, visited, path)
        return self.all_paths

def read_graph(utg):
    f = open(utg, 'r')
    parsed_json = json.loads(f.read())
    f.close()
    # read graph
    vertices = 0
    graph = []
    for event in parsed_json['events']:
        s = int(event['sourceScreenId'])
        d = int(event['destinationScreenId'])
        graph.append([s,d])
        if s > vertices:
            vertices = s
        if d > vertices:
            vertices = d
    # init graph
    g = Graph(vertices+1)
    for s, d in graph:
        g.addEdge(s, d)
    
    return g



def find_all_paths_in_graph(graph, s, d):
    return graph.printAllPaths(s, d)

def calulcate_lcs(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0 for x in range(n+1)] for x in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    index = L[m][n]
    lcs = [""] * (index+1)
    lcs[index] = ""
    i = m
    j = n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs[index-1] = X[i-1]
            i-=1
            j-=1
            index-=1
        elif L[i-1][j] > L[i][j-1]:
            i-=1
        else:
            j-=1
    lcs = lcs[:-1]
    return lcs

def find_execution_trace(utg, index_sequence):
    graph = read_graph(utg)
    paths = find_all_paths_in_graph(graph, 0, index_sequence[-1])
    # print('Find all paths')
    # print(paths)

    lcss = []
    max_lcs = 0
    max_lcs_paths = []
    # find longest LCS
    for path in paths:
        lcs = calulcate_lcs(path, index_sequence)
        lcss.append(lcs)
        if len(lcs) > max_lcs:
            max_lcs = len(lcs)
            max_lcs_paths = [path]
        elif len(lcs) == max_lcs:
            max_lcs_paths.append(path)
        else:
            pass
    # shortest execution trace
    # min(max_lcs_paths, key=len)
    execution_trace = [path for path in max_lcs_paths if len(path) == min(map(len, max_lcs_paths))]
    execution_trace.sort()
    execution_trace = list(k for k,_ in itertools.groupby(execution_trace))
    return execution_trace




if __name__ == "__main__":
    # Debug
    graph = Graph(9)
    graph.addEdge(0, 1)
    graph.addEdge(1, 2)
    graph.addEdge(2, 3)
    graph.addEdge(3, 4)
    graph.addEdge(4, 3)
    graph.addEdge(4, 5)
    graph.addEdge(5, 6)
    graph.addEdge(6, 1)
    graph.addEdge(2, 7)
    graph.addEdge(7, 8)
    graph.addEdge(8, 4)
    graph.addEdge(8, 5)
    index = [2,4,5]
    paths = find_all_paths_in_graph(graph, 0, index[-1])
    print(paths)
    trace = find_execution_trace(index, paths)
    print(trace)



    None
