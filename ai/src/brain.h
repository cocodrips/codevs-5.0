#ifndef AI_BRAIN_H
#define AI_BRAIN_H

#include "codevs.h"
#include "point.h"
#include "path.h"
#include "cell.h"
#include "state.h"

namespace Brain {

bool canMove(const State &state, const Point me, const Point direction);

int moveToDestination(State *state, Point *outMe, const vector<Point> &path,
                      vector<Point> *outGetSouls, const set<Point> &souls);

Point move(State *state, const Point me, const Point direction);

void setNextDogs(State *state);

int getDogScore(const State &state);

vector<Point> tryAllRelayPoint(const State &_state,
                               const Point &_me,
                               const Point &destination,
                               int step, set<Point> *outGetSouls);

int setBestPath(const State &state, int step,
                vector<Point> *outPath0,
                vector<Point> *outPath1, int initScore);

void simulate(const State &_state, string *outSkill,
              vector<Point> *outPath0, vector<Point> *outPath1);

}

#endif //AI_BRAIN_H
