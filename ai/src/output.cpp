#include "output.h"

char Output::directionToWord(const Point &point) {
    if (point == Point(-1, 0)) return 'U';
    if (point == Point(0, -1)) return 'L';
    if (point == Point(0, 1)) return 'R';
    if (point == Point(1, 0)) return 'D';
    if (point == Point(0, 0)) return 'N';
    return ' ';
}

string Output::pointsToWord(const vector<Point> &points) {
    string joined = "";
    for (const Point &point : points) {
        joined += directionToWord(point);
    }
    return joined;
}

void Output::mainOutput(Controller &controller, ostream &cout) {
    cout << 2 << endl;

    cout << pointsToWord(controller.myState.nextStep[0]) << endl;
    cout << pointsToWord(controller.myState.nextStep[1]) << endl;
}
