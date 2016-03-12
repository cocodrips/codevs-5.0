#ifndef AI_INPUT_H
#define AI_INPUT_H

#include "codevs.h"
#include "point.h"
#include "cell.h"
#include "controller.h"

namespace Input {
void playerInput(State *state, istream& cin);
void mainInput(Controller *controller, istream& cin);
}


#endif //AI_INPUT_H
