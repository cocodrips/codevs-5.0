#include "path.h"

const map<Point, vector<vector<Point>>> Path::destinations[] = {
        map<Point, vector<vector<Point>>>(),
        map<Point, vector<vector<Point>>>(),
        {{Point(0, 0), {{Point(-1, 0), Point(1, 0),}, {Point(0, -1), Point(0, 1),}, {Point(0, 1), Point(0, -1),},
                        {Point(1, 0), Point(-1, 0),}, {},}},
         {Point(0, 1), {{Point(0, 1),}, {Point(0, 1),},}},
         {Point(0, 2), {{Point(0, 1), Point(0, 1),},}},
         {Point(2, 0), {{Point(1, 0), Point(1, 0),},}},
         {Point(1, -1), {{Point(0, -1), Point(1, 0),}, {Point(1, 0), Point(0, -1),},}},
         {Point(1, 0), {{Point(1, 0),}, {Point(1, 0),},}},
         {Point(1, 1), {{Point(0, 1), Point(1, 0),}, {Point(1, 0), Point(0, 1),},}},
         {Point(-2, 0), {{Point(-1, 0), Point(-1, 0),},}},
         {Point(0, -2), {{Point(0, -1), Point(0, -1),},}},
         {Point(-1, -1), {{Point(-1, 0), Point(0, -1),}, {Point(0, -1), Point(-1, 0),},}},
         {Point(-1, 0), {{Point(-1, 0),}, {Point(-1, 0),},}},
         {Point(-1, 1), {{Point(-1, 0), Point(0, 1),}, {Point(0, 1), Point(-1, 0),},}},
         {Point(0, -1), {{Point(0, -1),}, {Point(0, -1),},}}
        },
        map<Point, vector<vector<Point>>>(),
};

const map<Point, vector<vector<Point>>> Path::paths[] = {
        map<Point, vector<vector<Point>>>(),
        map<Point, vector<vector<Point>>>(),
        {{Point(0, 0), {{Point(1, 0),}, {Point(-1, 0),}, {Point(0, -1),}, {Point(0, 1),}, {Point(0, 0),},}},
         {Point(0, 1), {{Point(0, 0),}, {Point(0, 1),},}},
         {Point(0, 2), {{Point(0, 1),},}},
         {Point(2, 0), {{Point(1, 0),},}},
         {Point(1, -1), {{Point(1, 0),}, {Point(0, -1),},}},
         {Point(1, 0), {{Point(1, 0),}, {Point(0, 0),},}},
         {Point(1, 1), {{Point(1, 0),}, {Point(0, 1),},}},
         {Point(-2, 0), {{Point(-1, 0),},}},
         {Point(0, -2), {{Point(0, -1),},}},
         {Point(-1, -1), {{Point(-1, 0),}, {Point(0, -1),},}},
         {Point(-1, 0), {{Point(-1, 0),}, {Point(0, 0),},}},
         {Point(-1, 1), {{Point(-1, 0),}, {Point(0, 1),},}},
         {Point(0, -1), {{Point(0, 0),}, {Point(0, -1),},}},
        },
        map<Point, vector<vector<Point>>>(),
};