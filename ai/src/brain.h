#ifndef AI_BRAIN_H
#define AI_BRAIN_H

#include "codevs.h"
#include "point.h"
#include "path.h"
#include "cell.h"
#include "state.h"

namespace Brain {

bool canDropBlock(const State &state, const Point &point);
Point cornerBlock(const State &state);
Point endMost(const vector<Point> &points);
Point level5Death(const State &_state);

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

int setBestPath(const State &state, const int step,
                vector<Point> *outPath0,
                vector<Point> *outPath1, int initScore);


Point dropBlockWorstPoint(const State &_state, const int scoreDiffThreshold);
int doppelBestPoint(const State &_state, const int scoreThreshold, string *outSkill,
                      vector<Point> *outPath0, vector<Point> *outPath1);

void simulate(const State &_state, const State &enemyState, string *outSkill,
              vector<Point> *outPath0, vector<Point> *outPath1);

}


#endif //AI_BRAIN_H
