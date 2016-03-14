#include "cell.h"

Cell::Cell() {
    type = Cell::Empty;
}

Cell::Cell(char c) {
    type = c;
}

bool Cell::isEmpty() const {
    return type == Empty;
}

bool Cell::isBlock() const {
    return type == Block;
}

bool Cell::isWall() const {
    return type == Wall;
}
