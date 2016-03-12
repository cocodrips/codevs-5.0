#ifndef AI_CONTROLLER_H
#define AI_CONTROLLER_H

#include "state.h"

class Controller {
public:
    State myState;
    State enemyState;

    Controller();
};


#endif //AI_CONTROLLER_H
