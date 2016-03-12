from ai.point import Point
import itertools


class Direction:
    directions = [Point(-1, 0), Point(0, -1), Point(0, 1), Point(1, 0), Point(0, 0)]
    arrows = {
        Point(-1, 0): "^",
        Point(0, -1): "<",
        Point(0, 1): ">",
        Point(1, 0): "v",
        Point(0, 0): " ",
    }

    @staticmethod
    def to_allow(point):
        return Direction.arrows[point]

    @staticmethod
    def all_directions(i):
        if i > 3:
            i = 3
        ds = []
        if i == 2:
            for d1 in Direction.directions:
                for d2 in Direction.directions:
                    ds.append((d1, d2))

        if i == 3:
            for d1 in Direction.directions:
                for d2 in Direction.directions:
                    for d3 in Direction.directions:
                        ds.append((d1, d2, d3))

        return ds


class Path:
    paths = [
        {},
        {},
        {
            Point(0, 0): [[Point(-1, 0), Point(1, 0), ], [Point(0, -1), Point(0, 1), ], [Point(0, 1), Point(0, -1), ],
                          [Point(1, 0), Point(-1, 0), ], [Point(0, 0), Point(0, 0), ], ],
            Point(0, 1): [[Point(0, 1), Point(0, 0), ], [Point(0, 0), Point(0, 1), ], ],
            Point(0, 2): [[Point(0, 1), Point(0, 1), ], ],
            Point(2, 0): [[Point(1, 0), Point(1, 0), ], ],
            Point(1, -1): [[Point(0, -1), Point(1, 0), ], [Point(1, 0), Point(0, -1), ], ],
            Point(1, 0): [[Point(1, 0), Point(0, 0), ], [Point(0, 0), Point(1, 0), ], ],
            Point(1, 1): [[Point(0, 1), Point(1, 0), ], [Point(1, 0), Point(0, 1), ], ],
            Point(-2, 0): [[Point(-1, 0), Point(-1, 0), ], ],
            Point(0, -2): [[Point(0, -1), Point(0, -1), ], ],
            Point(-1, -1): [[Point(-1, 0), Point(0, -1), ], [Point(0, -1), Point(-1, 0), ], ],
            Point(-1, 0): [[Point(-1, 0), Point(0, 0), ], [Point(0, 0), Point(-1, 0), ], ],
            Point(-1, 1): [[Point(-1, 0), Point(0, 1), ], [Point(0, 1), Point(-1, 0), ], ],
            Point(0, -1): [[Point(0, -1), Point(0, 0), ], [Point(0, 0), Point(0, -1), ], ],
        },
        {
            Point(0, 0): [[Point(-1, 0), Point(1, 0), Point(0, 0), ], [Point(-1, 0), Point(0, 0), Point(1, 0), ],
                          [Point(0, -1), Point(0, 1), Point(0, 0), ], [Point(0, -1), Point(0, 0), Point(0, 1), ],
                          [Point(0, 1), Point(0, -1), Point(0, 0), ], [Point(0, 1), Point(0, 0), Point(0, -1), ],
                          [Point(1, 0), Point(-1, 0), Point(0, 0), ], [Point(1, 0), Point(0, 0), Point(-1, 0), ],
                          [Point(0, 0), Point(-1, 0), Point(1, 0), ], [Point(0, 0), Point(0, -1), Point(0, 1), ],
                          [Point(0, 0), Point(0, 1), Point(0, -1), ], [Point(0, 0), Point(1, 0), Point(-1, 0), ],
                          [Point(0, 0), Point(0, 0), Point(0, 0), ], ],
            Point(0, 1): [[Point(-1, 0), Point(0, 1), Point(1, 0), ], [Point(-1, 0), Point(1, 0), Point(0, 1), ],
                          [Point(0, -1), Point(0, 1), Point(0, 1), ], [Point(0, 1), Point(-1, 0), Point(1, 0), ],
                          [Point(0, 1), Point(0, -1), Point(0, 1), ], [Point(0, 1), Point(0, 1), Point(0, -1), ],
                          [Point(0, 1), Point(1, 0), Point(-1, 0), ], [Point(0, 1), Point(0, 0), Point(0, 0), ],
                          [Point(1, 0), Point(-1, 0), Point(0, 1), ], [Point(1, 0), Point(0, 1), Point(-1, 0), ],
                          [Point(0, 0), Point(0, 1), Point(0, 0), ], [Point(0, 0), Point(0, 0), Point(0, 1), ], ],
            Point(0, 2): [[Point(0, 1), Point(0, 1), Point(0, 0), ], [Point(0, 1), Point(0, 0), Point(0, 1), ],
                          [Point(0, 0), Point(0, 1), Point(0, 1), ], ],
            Point(0, 3): [[Point(0, 1), Point(0, 1), Point(0, 1), ], ],
            Point(-3, 0): [[Point(-1, 0), Point(-1, 0), Point(-1, 0), ], ],
            Point(2, -1): [[Point(0, -1), Point(1, 0), Point(1, 0), ], [Point(1, 0), Point(0, -1), Point(1, 0), ],
                           [Point(1, 0), Point(1, 0), Point(0, -1), ], ],
            Point(2, 0): [[Point(1, 0), Point(1, 0), Point(0, 0), ], [Point(1, 0), Point(0, 0), Point(1, 0), ],
                          [Point(0, 0), Point(1, 0), Point(1, 0), ], ],
            Point(2, 1): [[Point(0, 1), Point(1, 0), Point(1, 0), ], [Point(1, 0), Point(0, 1), Point(1, 0), ],
                          [Point(1, 0), Point(1, 0), Point(0, 1), ], ],
            Point(-1, -2): [[Point(-1, 0), Point(0, -1), Point(0, -1), ], [Point(0, -1), Point(-1, 0), Point(0, -1), ],
                            [Point(0, -1), Point(0, -1), Point(-1, 0), ], ],
            Point(-1, -1): [[Point(-1, 0), Point(0, -1), Point(0, 0), ], [Point(-1, 0), Point(0, 0), Point(0, -1), ],
                            [Point(0, -1), Point(-1, 0), Point(0, 0), ], [Point(0, -1), Point(0, 0), Point(-1, 0), ],
                            [Point(0, 0), Point(-1, 0), Point(0, -1), ], [Point(0, 0), Point(0, -1), Point(-1, 0), ], ],
            Point(-1, 0): [[Point(-1, 0), Point(-1, 0), Point(1, 0), ], [Point(-1, 0), Point(0, -1), Point(0, 1), ],
                           [Point(-1, 0), Point(0, 1), Point(0, -1), ], [Point(-1, 0), Point(1, 0), Point(-1, 0), ],
                           [Point(-1, 0), Point(0, 0), Point(0, 0), ], [Point(0, -1), Point(-1, 0), Point(0, 1), ],
                           [Point(0, -1), Point(0, 1), Point(-1, 0), ], [Point(0, 1), Point(-1, 0), Point(0, -1), ],
                           [Point(0, 1), Point(0, -1), Point(-1, 0), ], [Point(1, 0), Point(-1, 0), Point(-1, 0), ],
                           [Point(0, 0), Point(-1, 0), Point(0, 0), ], [Point(0, 0), Point(0, 0), Point(-1, 0), ], ],
            Point(-1, 1): [[Point(-1, 0), Point(0, 1), Point(0, 0), ], [Point(-1, 0), Point(0, 0), Point(0, 1), ],
                           [Point(0, 1), Point(-1, 0), Point(0, 0), ], [Point(0, 1), Point(0, 0), Point(-1, 0), ],
                           [Point(0, 0), Point(-1, 0), Point(0, 1), ], [Point(0, 0), Point(0, 1), Point(-1, 0), ], ],
            Point(-1, 2): [[Point(-1, 0), Point(0, 1), Point(0, 1), ], [Point(0, 1), Point(-1, 0), Point(0, 1), ],
                           [Point(0, 1), Point(0, 1), Point(-1, 0), ], ],
            Point(1, -2): [[Point(0, -1), Point(0, -1), Point(1, 0), ], [Point(0, -1), Point(1, 0), Point(0, -1), ],
                           [Point(1, 0), Point(0, -1), Point(0, -1), ], ],
            Point(1, -1): [[Point(0, -1), Point(1, 0), Point(0, 0), ], [Point(0, -1), Point(0, 0), Point(1, 0), ],
                           [Point(1, 0), Point(0, -1), Point(0, 0), ], [Point(1, 0), Point(0, 0), Point(0, -1), ],
                           [Point(0, 0), Point(0, -1), Point(1, 0), ], [Point(0, 0), Point(1, 0), Point(0, -1), ], ],
            Point(1, 0): [[Point(-1, 0), Point(1, 0), Point(1, 0), ], [Point(0, -1), Point(0, 1), Point(1, 0), ],
                          [Point(0, -1), Point(1, 0), Point(0, 1), ], [Point(0, 1), Point(0, -1), Point(1, 0), ],
                          [Point(0, 1), Point(1, 0), Point(0, -1), ], [Point(1, 0), Point(-1, 0), Point(1, 0), ],
                          [Point(1, 0), Point(0, -1), Point(0, 1), ], [Point(1, 0), Point(0, 1), Point(0, -1), ],
                          [Point(1, 0), Point(1, 0), Point(-1, 0), ], [Point(1, 0), Point(0, 0), Point(0, 0), ],
                          [Point(0, 0), Point(1, 0), Point(0, 0), ], [Point(0, 0), Point(0, 0), Point(1, 0), ], ],
            Point(1, 1): [[Point(0, 1), Point(1, 0), Point(0, 0), ], [Point(0, 1), Point(0, 0), Point(1, 0), ],
                          [Point(1, 0), Point(0, 1), Point(0, 0), ], [Point(1, 0), Point(0, 0), Point(0, 1), ],
                          [Point(0, 0), Point(0, 1), Point(1, 0), ], [Point(0, 0), Point(1, 0), Point(0, 1), ], ],
            Point(1, 2): [[Point(0, 1), Point(0, 1), Point(1, 0), ], [Point(0, 1), Point(1, 0), Point(0, 1), ],
                          [Point(1, 0), Point(0, 1), Point(0, 1), ], ],
            Point(-2, -1): [[Point(-1, 0), Point(-1, 0), Point(0, -1), ], [Point(-1, 0), Point(0, -1), Point(-1, 0), ],
                            [Point(0, -1), Point(-1, 0), Point(-1, 0), ], ],
            Point(-2, 0): [[Point(-1, 0), Point(-1, 0), Point(0, 0), ], [Point(-1, 0), Point(0, 0), Point(-1, 0), ],
                           [Point(0, 0), Point(-1, 0), Point(-1, 0), ], ],
            Point(-2, 1): [[Point(-1, 0), Point(-1, 0), Point(0, 1), ], [Point(-1, 0), Point(0, 1), Point(-1, 0), ],
                           [Point(0, 1), Point(-1, 0), Point(-1, 0), ], ],
            Point(0, -1): [[Point(-1, 0), Point(0, -1), Point(1, 0), ], [Point(-1, 0), Point(1, 0), Point(0, -1), ],
                           [Point(0, -1), Point(-1, 0), Point(1, 0), ], [Point(0, -1), Point(0, -1), Point(0, 1), ],
                           [Point(0, -1), Point(0, 1), Point(0, -1), ], [Point(0, -1), Point(1, 0), Point(-1, 0), ],
                           [Point(0, -1), Point(0, 0), Point(0, 0), ], [Point(0, 1), Point(0, -1), Point(0, -1), ],
                           [Point(1, 0), Point(-1, 0), Point(0, -1), ], [Point(1, 0), Point(0, -1), Point(-1, 0), ],
                           [Point(0, 0), Point(0, -1), Point(0, 0), ], [Point(0, 0), Point(0, 0), Point(0, -1), ], ],
            Point(3, 0): [[Point(1, 0), Point(1, 0), Point(1, 0), ], ],
            Point(0, -3): [[Point(0, -1), Point(0, -1), Point(0, -1), ], ],
            Point(0, -2): [[Point(0, -1), Point(0, -1), Point(0, 0), ], [Point(0, -1), Point(0, 0), Point(0, -1), ],
                           [Point(0, 0), Point(0, -1), Point(0, -1), ], ],
        }]
    
    #TODO: かぶりなくす
    relay_points = [
        {},
        {},
        {
            Point( 0 , 0 ): {Point( -1 , 0 ),Point( 0 , 1 ),Point( 0 , -1 ),Point( 1 , 0 ),},
            Point( 0 , 1 ): {Point( 0 , 1 ),},
            Point( 0 , 2 ): {Point( 0 , 1 ),},
            Point( 2 , 0 ): {Point( 1 , 0 ),},
            Point( 1 , -1 ): {Point( 1 , 0 ),Point( 0 , -1 ),},
            Point( 1 , 0 ): {Point( 1 , 0 ),},
            Point( 1 , 1 ): {Point( 1 , 0 ),Point( 0 , 1 ),},
            Point( -2 , 0 ): {Point( -1 , 0 ),},
            Point( 0 , -2 ): {Point( 0 , -1 ),},
            Point( -1 , -1 ): {Point( -1 , 0 ),Point( 0 , -1 ),},
            Point( -1 , 0 ): {Point( -1 , 0 ),},
            Point( -1 , 1 ): {Point( -1 , 0 ),Point( 0 , 1 ),},
            Point( 0 , -1 ): {Point( 0 , -1 ),},
        },
        {
            Point( 0 , 0 ): {Point( -1 , 0 ),Point( 1 , 0 ),Point( 0 , 1 ),Point( 0 , -1 ),},
            Point( 0 , 1 ): {Point( -1 , 0 ),Point( 0 , 1 ),Point( 1 , 0 ),Point( 0 , -1 ),},
            Point( 0 , 2 ): {Point( 0 , 1 ),},
            Point( 0 , 3 ): {Point( 0 , 1 ),},
            Point( -3 , 0 ): {Point( -1 , 0 ),},
            Point( 2 , -1 ): {Point( 1 , 0 ),Point( 0 , -1 ),},
            Point( 2 , 0 ): {Point( 1 , 0 ),},
            Point( 2 , 1 ): {Point( 1 , 0 ),Point( 0 , 1 ),},
            Point( -1 , -2 ): {Point( -1 , 0 ),Point( 0 , -1 ),},
            Point( -1 , -1 ): {Point( -1 , 0 ),Point( 0 , -1 ),},
            Point( -1 , 0 ): {Point( -1 , 0 ),Point( 0 , 1 ),Point( 0 , -1 ),Point( 1 , 0 ),},
            Point( -1 , 1 ): {Point( -1 , 0 ),Point( 0 , 1 ),},
            Point( -1 , 2 ): {Point( -1 , 0 ),Point( 0 , 1 ),},
            Point( 1 , -2 ): {Point( 1 , 0 ),Point( 0 , -1 ),},
            Point( 1 , -1 ): {Point( 1 , 0 ),Point( 0 , -1 ),},
            Point( 1 , 0 ): {Point( -1 , 0 ),Point( 1 , 0 ),Point( 0 , -1 ),Point( 0 , 1 ),},
            Point( 1 , 1 ): {Point( 1 , 0 ),Point( 0 , 1 ),},
            Point( 1 , 2 ): {Point( 1 , 0 ),Point( 0 , 1 ),},
            Point( -2 , -1 ): {Point( -1 , 0 ),Point( 0 , -1 ),},
            Point( -2 , 0 ): {Point( -1 , 0 ),},
            Point( -2 , 1 ): {Point( -1 , 0 ),Point( 0 , 1 ),},
            Point( 0 , -1 ): {Point( -1 , 0 ),Point( 1 , 0 ),Point( 0 , -1 ),Point( 0 , 1 ),},
            Point( 3 , 0 ): {Point( 1 , 0 ),},
            Point( 0 , -3 ): {Point( 0 , -1 ),},
            Point( 0 , -2 ): {Point( 0 , -1 ),},
        }

    ]