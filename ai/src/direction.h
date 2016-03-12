#ifndef AI_DIRECTION_H
#define AI_DIRECTION_H

#include "point.h"

class Direction {
public:
    static const Point up;
    static const Point left;
    static const Point right;
    static const Point down;
    static const Point zero;
    static const Point directions[5];

    Direction();
};


#endif //AI_DIRECTION_H
