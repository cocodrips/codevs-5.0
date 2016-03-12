#ifndef AI_BRAIN_H
#define AI_BRAIN_H

#include "codevs.h"
#include "point.h"
#include "path.h"
#include "cell.h"
#include "state.h"

namespace Brain {

bool canMove(const State &state, const Point me, const Point direction);

Point move(State *state, const Point me, const Point direction);

void setNextDogs(State *state);
int getDogScore(const State &state);

vector<Point> tryAllRelayPoint(const State &_state,
                       const Point &_me,
                       const Point &direction,
                       int step, set<Point> *outGetSouls);

void setBestPath(const State &state, int step,
                 vector<Point> *outPath0, vector<Point> *outPath1);

void simulate(State *state, string *outSkill,
              vector<Point> *outPath0, vector<Point> *outPath1);

}

#endif //AI_BRAIN_H
