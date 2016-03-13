#ifndef AI_STATE_H
#define AI_STATE_H

#include "codevs.h"
#include "point.h"
#include "character.h"
#include "cell.h"
#include "direction.h"

class State {
public:
    int skillPower[Skill::Max];
    int skillUsed[Skill::Max];
    int power;
    vector<Character> ninjas;
    vector<vector<Cell>> field;
    set<Point> dogPoints;
    map<Point, Character>dogs;
    set<Point> souls;

    Point doppelganger;
    vector<Point> exceptions;

    vector<vector<Point> > nextStep;
    vector<vector<int> > stepsToNinjas;
    vector<vector<int> > stepsToDopperl;
    State();
    void setStepsToNinjas();

    void setStepsToDoppel(Point doppel);




    void start();

    void dumpField(ostream &cerr);

    set<int> distToNinja(const Point &pos) const;

    vector<vector<int>> stepsFromPoints(vector<Point> points);
    void dumpStepsToNinjas(ostream &cerr);
    void dumpStepsToDoppel(ostream &cerr);

private:
    void clearDogInfo();

    void clearSoul();


};


#endif //AI_STATE_H
