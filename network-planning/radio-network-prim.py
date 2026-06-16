def prak():
    import random
    import math
    r = int(input())


    class Station():
        def __init__(self,name,cords,points,dot_name):
            self.name = name
            self.cords = cords
            self.points = points
            self.dot_name = dot_name
        
        def __str__(self):
            if self.points:
                return f"{self.name,self.cords,[(x[0].name,x[1]) for x in self.points]}"
            else:
                return f"{self.name,self.cords}"

    class Point():
        def __init__(self,cords,name):
            self.cords = cords #(x,y)
            self.name = name
            self.nearest = []
            type = random.choice(["A","B","C"])
            self.pass_ab = {"C":250,"B":170,"A":150}[type]
            self.price = {"C":1000,"B":900,"A":750}[type] #per 100m
        
        def __str__(self):
            if self.nearest:
                return f"{self.name,self.cords,[(x[0].name,x[1]) for x in self.nearest]}"
            else:
                return f"{self.name,self.cords}"
        
        def __gt__(self,other):
            return len(self.nearest) > len(other.nearest)
        
        def __lt__(self,other):
            return len(self.nearest) < len(other.nearest)
        
        def __add__(self,other:"Point"):
            return self.pass_ab + other.pass_ab
            
    class Tree():
        def __init__(self, points, head):
            self.points = points
            self.head = head #where the station is
            
    points:list[Point] = []
    cords = []
    for i in range(10):
        cor = (random.randint(0,10),random.randint(0,10))
        while cor in cords:
            cor = (random.randint(0,10),random.randint(0,10))
        new = Point(cor,str(i))
        points.append(new)
        cords.append(cor)

    for i in range(len(points)):
        for j in range(i+1,len(points)):
            length = math.sqrt(abs(points[i].cords[0] - points[j].cords[0])**2 + abs(points[i].cords[1]-points[j].cords[1])**2)
            if  length <= r:
                points[i].nearest.append([points[j],round(length,2)])
                points[j].nearest.append([points[i],round(length,2)])

    def check(points,req):
        ss = {x: x.pass_ab for x in points}
        if sum(ss.values()) > 1024-req.pass_ab:
            nums = sorted(ss.items(), reverse=True)
            # print(nums)
            total = 0
            result = []
            for x in nums:
                if total + x[1] <= 1024-req.pass_ab:
                    result.append(x[0])
                    total += x[1]
            return [req]+result
        return [req]+list(ss.keys())
        

    def set_stations(points:list):
        stations = []
        available:list[Point] = points.copy()
        n = -1
        
        

        while available:
            n += 1
            points = []
            # print(list(map(lambda x: x[0].name,max(available).nearest)))
            m = max(available)
            for p in m.nearest:
                if p[0] in available:
                    points.append(p[0])
            
            points = check(points,m)
            
            new = Station(str(n),m.cords,points,m)
            stations.append(new)
            for dot in points:
                if dot in available:
                    available.remove(dot)

        
        return stations


    stations:list[Station] = set_stations(points) #[Station]
    # print(list(map(lambda x: (x.dot_name.name,list(map(lambda c: c.name,x.points))),stations)))
    # print(points)
    # print(points)
    # print(cords)



    def count_distance(A:Point,B:Point):
        return round(math.sqrt(abs(A.cords[0] - B.cords[0])**2 + abs(A.cords[1]-B.cords[1])**2),2)


    from collections import defaultdict
    def make_graph(station:Station):
        if len(station.points) == 1:
            return 0
        graph = defaultdict(list)
        for p in station.points:
            p = p
            for m in station.points:
                m = m
                if p != m:
                    graph[p].append((m,round(count_distance(p,m)*m.price*5000)))
        # print(graph)
        return dict(graph)



    graphs = []
    for i in range(len(stations)):
        graphs.append((stations[i].dot_name,make_graph(stations[i])))



    import heapq


    def prima(graph,start):
        mst = [] #list of edges
        visited = set() #cheked points
        heap = [] #priority queue

        visited.add(start)
        for neighbor, weight in graph[start]:
            heapq.heappush(heap, (weight,start,neighbor))
        
        while heap:
            weight,start,end = heapq.heappop(heap)
            if end not in visited:
                visited.add(end)
                mst.append((start,end,weight))

                for neighbor, weight in graph[end]:
                    if neighbor not in visited:
                        heapq.heappush(heap, (weight,end,neighbor))
        return mst




    for graph in graphs:
        
        if graph[1] != 0:
            mst = prima(graph[1],graph[0])
            for start,end,weight in mst:

                print(f"{start.name} - {end.name} : {weight}")
        else:
            print(graph[0].name, "(graph consists of 1 dot)")
        print()
        
    
    
        
    print("\n\n")
    print("points в формате - (имя, координаты, точки, которые лежат в данном радусе от этой точки (маштаб 1:5)) :")
    for point in points:
        print(point)
    

prak()