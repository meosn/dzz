from collections import deque

matrix = [
    [0,1],
    [-1,0]
    ]
n = len(matrix)
edges = {
(0, 0): [(0,1), (1, 1)],
(0, 1): [(0, 0), (1, 1)],
(1, 1): [(0, 0), (0, 1)]
}

class Graph():
    def __init__(self):
        self.edges = {}
    def add_node(self,node):
        if node not in self.edges:
            self.edges[node] = []
    def add_edge(self,from_node,to_node):
        self.edges[from_node].append(to_node)
    def show_time(self,start_node,final_node):
        dist = {}
        for x in self.edges:
            pass
               
            
        
def matrix_to_graph(matrix):
    graph = Graph()
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] != -1:
                graph.add_node((x,y))
                for d in directions:
                    if x + d[0] >= 0 and y + d[1] >= 0 and x + d[0] <= n and y + d[1] <= n:
                        graph.add_edge((x,y),(x + d[0],y + d[1]))
    return graph
graph  = matrix_to_graph(matrix)
print(graph.edges)
