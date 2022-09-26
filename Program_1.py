import numpy as np
from math import sqrt


class Node:

    # city name, longitude, latitude, and adjacencies
    def __init__(self, name, x, y):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.adjacents = set()
        self.visited = False
        self.previous = None
        self. obstacle = False

    # Euclidean distance using linalg.norm(), numpy arrays
    # https://www.delftstack.com/howto/numpy/calculate-euclidean-distance/
    def distance(self, other):
        point1 = np.array([self.x, self.y])
        point2 = np.array([other.x, other.y])
        dist = np.linalg.norm(point1 - point2)
        return dist


# Reference: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
def get_cities():
    cities = {}

    # Read the text file(coordinates.text)
    with open("coordinates.txt", "r") as coordinates:
        for line in coordinates.readlines():
            city = Node(*line.split())
            cities[city.name] = city
        # if city: print(city[0])

    # Read the text file(Adjacencies.text)
    with open("Adjacencies.txt", "r") as adjacencies:
        for line in adjacencies.readlines():
            line = line.split()
            begin = line[0]
            adj = []  # Adjacent cities

            for city in line:
                if (begin == city or (city not in cities)):
                    continue
                adj.append(city)

                for city in adj:
                    if (city not in cities[begin].adjacents):
                        cities[city].adjacents.add(begin)

            for city in adj:
                cities[begin].adjacents.add(city)

    return cities


cities = get_cities()
path = []
end_node = None

# User inputs the city names
while True:
    begin = input("Start City: ").capitalize()
    goal = input("Goal City: ").capitalize()
    if (begin not in cities or goal not in cities):
        print("Choose another city name.")
        continue
    break

current_node = cities[begin]

# Resorce used: https://www.redblobgames.com/pathfinding/a-star/introduction.html
# Run this while the current_node != goal_node
while True:

    # Frontier node close to the goal node
    frontier = cities[current_node.name].adjacents
    closest = {
        "name": None,
        "distance": float("inf")
    }

    for city in frontier:
        if (city in path or city == end_node):
            continue

        distance = cities[city].distance(cities[goal])
        if (distance < closest["distance"]):
            closest["name"] = city
            closest["distance"] = distance

        # try:
        #     result = path.pop()
        #     print(result)
        # except IndexError:
        #     #  this runs
        #     print('list is empty')
        #     print(len(path))
        #     path.append("singapore")

    if (closest["name"] is None):
        end_node = current_node.name
        path.pop()
        current_node = cities[path[-1]]
        continue
    else:
        path.append(closest["name"])
        current_node = cities[closest["name"]]

    # If the goal has been found, print it
    if (current_node.name == goal):
        print("Route has found!")
        print(begin + " -> " + " -> ".join(path))
        break
