#ifndef AI_CELL_H
#define AI_CELL_H

#include "point.h"
class Cell {
public:
    static const char Empty = '_';
    static const char Block = 'O';
    static const char Wall = 'W';
    char type;

    Cell ();
    Cell (char c) ;

    bool isEmpty () const;

    bool isBlock () const;

    bool isWall() const;
};

#endif //AI_CELL_H
