from ai import *
import collections


def get_all_destinaton(n):
    dests = collections.defaultdict(list)
    for directions in Direction.all_directions(n):
        dest = Point(0, 0)
        for direction in directions:
            dest += direction
        dests[dest].append(directions)
    return dests


step = 2

for dest, paths in get_all_destinaton(step).items():
    print("Point(", dest.y, ",", dest.x, "): [", end="")
    for path in paths:
        print("\t[", end="")
        for d in path:
            print("Point(", d.y, ",", d.x, "),", end="")
        print("\t],", end="")
    print("],")


# Relay point 
for dest, paths in get_all_destinaton(step).items():
    print("Point(", dest.y, ",", dest.x, "): {", end="")
    s = set()
    for path in paths:
        for d in path[:-1]:
            s.add(d)

    if Point(0,0) in s:
        s.remove(Point(0,0))

    for d in s:
        print("Point(", d.y, ",", d.x, "),", end="") 
    print("},")
