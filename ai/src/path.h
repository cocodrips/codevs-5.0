#ifndef AI_PATH_H
#define AI_PATH_H

#include "codevs.h"
#include "point.h"

class Path {
public:
    static const map<Point, vector<vector<Point>>> destinations[4];
    static const map<Point, vector<vector<Point>>> paths[4];
};


#endif //AI_PATH_H
