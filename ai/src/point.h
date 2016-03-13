#ifndef AI_POINT_H
#define AI_POINT_H

#include "codevs.h"


class Point {
public:
    int y;
    int x;

    Point();
    Point(int _y, int _x);
    bool operator==(const Point &other) const;
    bool operator!=(const Point &other) const;
    Point operator+(const Point &other) const;
    Point &operator+=(const Point &other);
    Point operator-(const Point &other) const;
    bool operator<(const Point &other) const;
    int dist(const Point &other) const;
    string print() const;
    bool isInsideField() const;


};


#endif //AI_POINT_H
