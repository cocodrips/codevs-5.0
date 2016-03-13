#include "controller.h"

Controller::Controller(){}

void Controller::think(string *outSkill, vector<Point> *outPath0, vector<Point> *outPath1) {
    Brain::simulate(myState, outSkill, outPath0, outPath1);
}