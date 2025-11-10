from collections import deque
from math import sqrt

matrix = [
    [0,  1],
    [-1, 0]
]

speeds = {0: 10.0, 1: 7.5, 2: 5.0}

rows, cols = len(matrix), len(matrix[0])

class Graph:
    def __init__(self):
        self.edges = {}

    def add_node(self, node):
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, u, v, w):
        self.edges[u].append((v, w))

    def __build_path(self, parent, finish):
        path, cur = [], finish
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path

    def show_path(self, data):
        parent = data["parent"]
        finish = data["finish"]
        return self.__build_path(parent, finish)

    def shortest_time(self, start, finish, mode='time'):
        if start not in self.edges or finish not in self.edges:
            return None

        m = float('inf')
        dist = {v: m for v in self.edges}
        parent = {v: None for v in self.edges}
        dist[start] = 0.0
        q = deque([start])
        in_q = {v: False for v in self.edges}
        in_q[start] = True      
        while q:
            u = q[0]
            best = dist[u]
            idx = 0
            for i in range(1, len(q)):
                if dist[q[i]] < best:
                    best = dist[q[i]]
                    u = q[i]
                    idx = i
            del q[idx]
            in_q[u] = False

            if u == finish:
                break

            for v, w in self.edges.get(u, []):
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd
                    parent[v] = u
                    if not in_q[v]:
                        q.append(v)
                        in_q[v] = True

        if dist[finish] == m:
            return None

        total = round(dist[finish], 2)

        if mode == 'time':
            return total
        elif mode == 'both':
            return total, self.__build_path(parent, finish)
        elif mode == 'struct':
            return total, {"parent": parent, "finish": finish}
        else:
            return total, self.__build_path(parent, finish)


def matrix_to_graph():
    g = Graph()
    dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

    for x in range(rows):
        for y in range(cols):
            if matrix[x][y] != -1:
                g.add_node((x, y))

    for x in range(rows):
        for y in range(cols):
            if matrix[x][y] == -1:
                continue
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < rows and 0 <= ny < cols):
                    continue
                if matrix[nx][ny] == -1:
                    continue

                dist = 10.0 if (dx == 0 or dy == 0) else round(10.0 * sqrt(2), 2)

                ta, tb = matrix[x][y], matrix[nx][ny]
                sa = speeds[ta]
                sb = speeds[tb]

                if ta == tb:
                    t = dist / sa
                else:
                    t = (dist / 2.0) / sa + (dist / 2.0) / sb

                w = round(t, 2)
                g.add_edge((x, y), (nx, ny), w)
                g.add_edge((nx, ny), (x, y), w)

    return g


g = matrix_to_graph()
start, finish = (0, 0), (1, 1)

print(g.shortest_time(start, finish, mode='time'))

print(g.shortest_time(start, finish, mode='both'))

t, data = g.shortest_time(start, finish, mode='struct')
print(t)
print(g.show_path(data))
