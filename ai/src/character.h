#ifndef AI_CHARACTER_H
#define AI_CHARACTER_H

#include "point.h"
class Character {
public:
    Point point;
    Character();

    Character(int id, int y, int x);

    bool operator==(const Character &other) const;
};

#endif //AI_CHARACTER_H
