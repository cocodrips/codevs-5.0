#ifndef AI_CHARACTER_H
#define AI_CHARACTER_H

#include "point.h"
class Character {
public:
    Point point;
    int id;
    int dist;
    Character();

    Character(int _id, int y, int x);

    bool operator==(const Character &other) const;
    bool operator<(const Character &other) const;
};

#endif //AI_CHARACTER_H
