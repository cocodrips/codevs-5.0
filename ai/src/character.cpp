#ifndef AI_CHARACTER
#define AI_CHARACTER

#include "character.h"

Character::Character() { };

Character::Character(int id, int y, int x) {
    point = Point(y, x);
}

bool Character::operator==(const Character &other) const {
    return this->point == other.point;
}


#endif
