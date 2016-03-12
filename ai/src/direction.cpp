#include "direction.h"

Direction::Direction() { }

const Point Direction::up(-1, 0);
const Point Direction::left = Point(0, -1);
const Point Direction::right = Point(0, 1);
const Point Direction::down = Point(1, 0);
const Point Direction::zero = Point(0, 0);
const Point Direction::directions[5] = {Direction::up, Direction::left,
                                        Direction::right, Direction::down,
                                        Direction::zero};

