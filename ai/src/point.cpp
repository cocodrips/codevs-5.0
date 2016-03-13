#include "point.h"

Point::Point() {
    y = -1;
    x = -1;
}

Point::Point(int _y, int _x) {
    y = _y;
    x = _x;
}

bool Point::operator==(const Point &other) const {
    return y == other.y && x == other.x;
}

bool Point::operator!=(const Point &other) const {
    return !(*this == other);
}

Point Point::operator+(const Point &other) const {
    return Point(y + other.y, x + other.x);
}

Point &Point::operator+=(const Point &other) {
    y += other.y;
    x += other.x;
    return *this;
}

Point Point::operator-(const Point &other) const {
    return Point(y - other.y, x - other.x);
}

bool Point::operator<(const Point &other) const {
    if (y == other.y) {
        return x < other.x;
    }
    return y < other.y;
}

int Point::dist(const Point &other) const {
    return abs(y - other.y) + abs(x - other.x);
}

string Point::print() const {
    if (abs(x) + abs(y) == 1) {
        if (x == 1) return "→";
        if (x == -1) return "←";
        if (y == 1) return "↓";
        if (y == -1) return "↑";
    }
    return "P(" + to_string(y) + ", " + to_string(x) + ")";
}

bool Point::isInsideField() const {
    return 0 <= y && y < Y && 0 <= x && x < X;
}