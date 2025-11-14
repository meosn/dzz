from dataclasses import dataclass
from math import radians, sin, cos, asin, sqrt, ceil, floor
import heapq


@dataclass
class Plane:
    tank_capacity: int
    fuel_consumption: float
    cruise_speed: float


@dataclass
class City:
    name: str
    lat: float
    lon: float
    has_fuel: bool


@dataclass
class Edge:
    to_city: str
    distance_km: float
    headwind: bool
    fairwind: bool
    closed: bool = False


class Graph:
    def __init__(self):
        self.cities = {}
        self.adj = {}

    def add_city(self, city: City):
        self.cities[city.name] = city
        if city.name not in self.adj:
            self.adj[city.name] = []

    def add_edge(self, from_city: str, edge: Edge):
        if from_city not in self.adj:
            self.adj[from_city] = []
        self.adj[from_city].append(edge)


def haversine_km(city_a: City, city_b: City):
    R = 6371.0
    lat1, lon1 = radians(city_a.lat), radians(city_a.lon)
    lat2, lon2 = radians(city_b.lat), radians(city_b.lon)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    distance = R * c
    return float(ceil(distance))


def heuristic_time(graph: Graph, plane: Plane, from_city: str, to_city: str):
    if from_city == to_city:
        return 0.0
    city_a = graph.cities[from_city]
    city_b = graph.cities[to_city]
    dist = haversine_km(city_a, city_b)
    max_speed = plane.cruise_speed * 1.1
    if max_speed == 0:
        return 0.0
    return dist / max_speed


def edge_costs(plane: Plane, edge: Edge):
    distance = edge.distance_km
    if edge.headwind:
        speed_factor = 0.8
        fuel_factor = 1.2
    elif edge.fairwind:
        speed_factor = 1.1
        fuel_factor = 0.9
    else:
        speed_factor = 1.0
        fuel_factor = 1.0
    effective_speed = plane.cruise_speed * speed_factor
    effective_consumption = plane.fuel_consumption * fuel_factor
    time_hours = distance / effective_speed
    fuel_used = distance * effective_consumption
    return time_hours, fuel_used


def astar_flight(graph: Graph, plane: Plane, start: str, goal: str):
    start_fuel = plane.tank_capacity
    start_state = (start, start_fuel)

    g = {start_state: 0.0}
    parent = {start_state: (None, None)}

    open_heap = []
    h0 = heuristic_time(graph, plane, start, goal)
    f0 = g[start_state] + h0
    heapq.heappush(open_heap, (f0, start, start_fuel))

    closed = set()
    goal_state = None

    while open_heap:
        _, city, fuel = heapq.heappop(open_heap)
        state = (city, fuel)

        if state in closed:
            continue
        closed.add(state)

        current_time = g[state]

        if city == goal:
            goal_state = state
            break

        current_city = graph.cities[city]

        if current_city.has_fuel and fuel < plane.tank_capacity:
            next_state = (city, plane.tank_capacity)
            refuel_time = 0.5
            new_time = ceil((current_time + refuel_time) * 10) / 10.0
            if next_state not in g or new_time < g[next_state]:
                g[next_state] = new_time
                parent[next_state] = (
                    state,
                    {"type": "refuel", "city": city, "time": refuel_time},
                )
                h = heuristic_time(graph, plane, city, goal)
                f = new_time + h
                heapq.heappush(open_heap, (f, next_state[0], next_state[1]))

        for edge in graph.adj.get(city, []):
            if edge.closed:
                continue

            time_edge, fuel_used = edge_costs(plane, edge)
            if fuel < fuel_used:
                continue

            new_fuel = int(floor(fuel - fuel_used))
            next_state = (edge.to_city, new_fuel)
            new_time = ceil((current_time + time_edge) * 10) / 10.0

            if next_state not in g or new_time < g[next_state]:
                g[next_state] = new_time
                parent[next_state] = (
                    state,
                    {
                        "type": "flight",
                        "from": city,
                        "to": edge.to_city,
                        "distance_km": edge.distance_km,
                        "time": time_edge,
                        "fuel_used": fuel_used,
                    },
                )
                h = heuristic_time(graph, plane, edge.to_city, goal)
                f = new_time + h
                heapq.heappush(open_heap, (f, next_state[0], next_state[1]))

    if goal_state is None:
        raise ValueError("Маршрут не найден")

    steps = []
    curr = goal_state
    while curr is not None:
        prev, action = parent[curr]
        steps.append((curr, action))
        curr = prev
    steps.reverse()

    path_cities = []
    details = []
    total_distance = 0.0
    refuel_count = 0

    for i, (state, action) in enumerate(steps):
        city_name, fuel = state
        if i == 0:
            path_cities.append(city_name)
            continue

        if action["type"] == "refuel":
            refuel_count += 1
            t = ceil(action["time"] * 10) / 10.0
            details.append(f"[Refuel {action['city']}] : +{t} ч")
        elif action["type"] == "flight":
            from_city = action["from"]
            to_city = action["to"]
            dist = action["distance_km"]
            time_raw = action["time"]
            t = ceil(time_raw * 10) / 10.0
            fuel_used = action["fuel_used"]
            details.append(
                f"{from_city} -> {to_city} : {t} ч, расход {ceil(fuel_used)} л"
            )
            total_distance += dist
            if path_cities[-1] != to_city:
                path_cities.append(to_city)

    total_time = g[goal_state]

    return path_cities, total_time, details, total_distance, refuel_count


plane = Plane(
    tank_capacity=16000,
    fuel_consumption=2.7,
    cruise_speed=841.0,
)

graph = Graph()

city_a = City("A", lat=55.75, lon=37.62, has_fuel=True)
city_b = City("B", lat=59.93, lon=30.31, has_fuel=True)
city_c = City("C", lat=52.52, lon=13.40, has_fuel=False)

for c in (city_a, city_b, city_c):
    graph.add_city(c)

graph.add_edge("A", Edge(to_city="B", distance_km=700.0, headwind=False, fairwind=True, closed=False))
graph.add_edge("B", Edge(to_city="C", distance_km=1300.0, headwind=True, fairwind=False, closed=False))
graph.add_edge("A", Edge(to_city="C", distance_km=1900.0, headwind=False, fairwind=False, closed=False))

path, total_time, details, total_distance, refuels = astar_flight(graph, plane, "A", "C")

print("Маршрут:", " -> ".join(path))
print("Шаги:")
for d in details:
    print(" ", d)
print(f"Итого: {total_time} ч, расстояние {total_distance} км, дозаправок: {refuels}")
