#ifndef AI_STATE
#define AI_STATE

#include "state.h"

State::State() { }

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
        REP(x, X) {
            cell = field[y][x];
            point = Point(y, x);
            char c = ' ';
            if (cell.isWall()) {
                c = 'W';
            } else if (cell.isBlock()) {
                c = 'O';
            } else if (dogPoints.find(point) != dogPoints.end()) {
                c = 'x';
            } else if (point == ninjas[0].point) {
                c = '1';
            } else if (point == ninjas[1].point) {
                c = '2';
            }
            cerr << c;
        }
        cerr << endl;
    }
}

void State::clearDogInfo() {
    dogPoints.clear();
    dogs.clear();
}

void State::clearSoul() {
    souls.clear();
}

#endif