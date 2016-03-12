#ifndef AI_CHARACTER
#define AI_CHARACTER

#include "character.h"

Character::Character() { };

Character::Character(int _id, int y, int x) {
    point = Point(y, x);
    id = _id;
}

bool Character::operator==(const Character &other) const {
    return this->point == other.point;
}

bool Character::operator<(const Character &other) const {
    return id < other.id;
}


#endif
