#ifndef AI_STATE
#define AI_STATE

#include "state.h"

State::State() : ninjas(NINJA_NUM), nextStep(NINJA_NUM), doppelganger() {
    field = vector<vector<Cell>>(Y);
    REP(i, Y) {
        field[i] = vector<Cell>(X);
    }


}

void State::start() {
    clearDogInfo();
    clearSoul();

    doppelganger = Point();
    exceptions.clear();

    nextStep[0].clear();
    nextStep[1].clear();
}

void State::dumpField(ostream &cerr) {
    Cell cell;
    Point point;
    stringstream ss;
    REP(y, Y) {
        cerr << setw(2) << y;
        REP(x, X) {
            cell = field[y][x];
            point = Point(y, x);
            string c = "";
            if (cell.isWall()) {
                c = "W";
            } else if (cell.isBlock()) {
                c = "O";
            } else if (dogPoints.find(point) != dogPoints.end()) {
                c = "x";
            } else {
                c = "_";
            }

            if (point == ninjas[0].point) {
                c += "1";
            } else if (point == ninjas[1].point) {
                c += "2";
            } else if (point == doppelganger) {
                c += "#";
            } else {
                c += " ";
            }
            cerr << setw(2) << c;
        }
        cerr << endl;
    }
}

set<int> State::distToNinja(const Point &pos) const {
    set<int> dists;
    dists.insert(ninjas[0].point.dist(pos));
    dists.insert(ninjas[1].point.dist(pos));
    return dists;
}

void State::clearDogInfo() {
    dogPoints.clear();
    dogs.clear();
}

void State::clearSoul() {
    souls.clear();
}

void State::setStepsToNinjas() {
    vector<Point> ninjaPoints;
    ninjaPoints.push_back(ninjas[0].point);
    ninjaPoints.push_back(ninjas[1].point);
    stepsToNinjas = stepsFromPoints(ninjaPoints);
}

void State::setStepsToDoppel(Point doppel) {
    vector<Point> points;
    points.push_back(doppel);
    stepsToDopperl = stepsFromPoints(points);
}

void State::setStepsToReachableCellFromNinja() {
    vector<Point> ninjaPoint;

    ninjaPoint.push_back(ninjas[0].point);
    ninjaPoint.push_back(ninjas[1].point);
    stepsToReachableCellNinjas = stepsToReachableCell(ninjaPoint);

}

vector<vector<int>> State::stepsToReachableCell(vector<Point> points) {
    vector<vector<int>> steps(Y);
    // 初期化
    REP (y, Y) {
        steps[y] = vector<int>(X);
        REP(x, X) {
            steps[y][x] = INF;
        }
    }

    set<Point> visited;
    priority_queue<tuple<int, Point>, vector<tuple<int, Point>>, greater<tuple<int, Point>>> queue; //dist, point
    for (Point p : points) {
        queue.push(make_tuple(0, p));
        visited.insert(p);
    }

    while (!queue.empty()) {
        tuple<int, Point> q = queue.top();
        queue.pop();

        int step = get<0>(q);
        Point point = get<1>(q);

        steps[point.y][point.x] = step;

        REP(i, DIRECTION_NUM) {
            Point d = Direction::directions[i];
            Point next = point + d;
            if (field[next.y][next.x].isWall()) continue;
            if (dogPoints.find(next) != dogPoints.end()) continue;          // 犬は壁
            if (field[next.y][next.x].isBlock()) {
                Point nextnext = next + d;
                if (field[nextnext.y][nextnext.x].isBlock()) continue;      // 石石は壁
                if (dogPoints.find(nextnext) != dogPoints.end()) continue;  // 石犬も壁
                //本当は石忍者も壁
                if (field[nextnext.y][nextnext.x].isEmpty()) {              // 石空?は壁
                    Point nnn = nextnext + d;
                    if (!field[nnn.y][nnn.x].isEmpty()) continue;
                    if (dogPoints.find(nnn) != dogPoints.end()) continue;
                }
            }
            if (visited.find(next) == visited.end()) {
                visited.insert(next);
                queue.push(make_tuple(step + 1, next));
            }

        }

    }
    return steps;
}

vector<vector<int>> State::stepsFromPoints(vector<Point> points) {
    vector<vector<int>> steps(Y);
    REP (y, Y) {
        steps[y] = vector<int>(X);
        REP(x, X) {
            steps[y][x] = INF;
        }
    }

    set<Point> visited;
    priority_queue<tuple<int, Point>, vector<tuple<int, Point>>, greater<tuple<int, Point>>> queue; //dist, point
    for (Point p : points) {
        queue.push(make_tuple(0, p));
        visited.insert(p);
    }

    while (!queue.empty()) {
        tuple<int, Point> q = queue.top();
        queue.pop();

        int step = get<0>(q);
        Point point = get<1>(q);

        steps[point.y][point.x] = step;

        REP(i, DIRECTION_NUM) {
            Point d = Direction::directions[i];
            Point next = point + d;
            if (!field[next.y][next.x].isEmpty()) continue;
            if (visited.find(next) == visited.end()) {
                visited.insert(next);
                queue.push(make_tuple(step + 1, next));
            }

        }

    }
    return steps;
}

void State::dumpStepsToNinjas(ostream &cerr) {

    REP(y, Y) {
        REP(x, X) {
            cerr << setw(2);

            if (stepsToNinjas[y][x] == INF) {
                cerr << "__";
            } else if (souls.find(Point(y, x)) != souls.end()) {
                cerr << "@";
            } else {
                cerr << stepsToNinjas[y][x];
            }
            cerr << " ";
        }
        cerr << endl;
    }
}

void State::dumpStepsToDoppel(ostream &cerr) {

    REP(y, Y) {
        REP(x, X) {
            cerr << setw(2);

            if (stepsToDopperl[y][x] == INF) {
                cerr << "__";
            } else if (souls.find(Point(y, x)) != souls.end()) {
                cerr << "@";
            } else {
                cerr << stepsToDopperl[y][x];
            }
            cerr << " ";
        }
        cerr << endl;
    }
}


#endif