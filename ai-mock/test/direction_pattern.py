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


step = 3

for dest, paths in get_all_destinaton(step).items():
    print("{Point(", dest.y, ",", dest.x, "), {", end="")
    for path in paths:
        print("\t{", end="")
        for d in path:
            if d == Point(0, 0):
                continue
            print("Point(", d.y, ",", d.x, "),", end="")
        print("},", end="")
    print("}},")


# Relay point 
# for dest, paths in get_all_destinaton(step).items():
#     print("{Point(", dest.y, ",", dest.x, "), {", end="")
#     s = set()
#     for path in paths:
#         s.add(path[:-1])
#     # 
#     # if Point(0,0) in s:
#     #     s.remove(Point(0,0))
# 
#     for p in s:
#         print("{", end="")
#         for d in p:
#             print("Point(", d.y, ",", d.x, "),", end="")
#         print("},", end="")
#     print("}},")
