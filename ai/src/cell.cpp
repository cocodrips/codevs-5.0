#include "cell.h"

Cell::Cell() {
    type = Cell::Empty;
}

Cell::Cell(char c) {
    type = c;
}

bool Cell::isEmpty() {
    return type == Empty;
}

bool Cell::isBlock() {
    return type == Block;
}

bool Cell::isWall() {
    return type == Wall;
}
