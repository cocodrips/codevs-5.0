#ifndef AI_CONTROLLER_H
#define AI_CONTROLLER_H

#include "state.h"
#include "brain.h"

class Controller {
public:
    State myState;
    State enemyState;

    Controller();

    void think(string *outSkill,
               vector<Point> *outPath0, vector<Point> *outPath1);
};

#endif //AI_CONTROLLER_H
