#ifndef AI_STATE_H
#define AI_STATE_H

#include "codevs.h"
#include "character.h"
#include "cell.h"

class State {
public:
    int skillPower[Skill::Max];
    int skillUsed[Skill::Max];
    int power;
    Character ninjas[NINJA_NUM];
    Cell field[Y][X];
    set<Point> dogPoints;
    map<Point, Character> dogs;
    set<Point> souls;

    Point doppelganger;
    vector<Point> exceptions;

    vector<Point> nextStep[NINJA_NUM];


    State();

    void start() ;

    void dumpField(ostream &cerr) ;

private:
    void clearDogInfo() ;

    void clearSoul() ;
};


#endif //AI_STATE_H
