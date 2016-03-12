#ifndef AI_OUTPUT_H
#define AI_OUTPUT_H

#include "controller.h"
#include "point.h"
namespace Output {

char directionToWord(const Point &point);
string pointsToWord(const vector<Point> &points);

void mainOutput(Controller *controller, ostream &cout);

};


#endif //AI_OUTPUT_H
