#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <climits>

using namespace std;

namespace codevs {

///////////////////////////////////////////////////////////////////
const int INF = 876765346;

const char CELL_EMPTY = '_';
const char CELL_WALL = 'W';
const char CELL_ROCK = 'O';

class Point {
public:
    int x, y;

    Point() { x = y = -1; }

    Point(int x, int y) : x(x), y(y) { }

    bool operator==(const Point &p) const { return x == p.x && y == p.y; }
};


class Character : public Point {
public:
    int id;

    Character() { id = -1; }

    Character(int id, int x, int y) : id(id), Point(x, y) { }
};

class Field {
public:

};

class Controller {
public:
    void input()
};


}