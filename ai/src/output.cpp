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

void Output::mainOutput(Controller *controller, ostream &cout) {
    cout << 2 << endl;
    string skill;
    vector<Point> path0;
    vector<Point> path1;
    controller->think(&skill, &path0, &path1);
    int size0 = path0.size();
    int size1 = path1.size();
    cout << pointsToWord(path0) << endl;
    cout << pointsToWord(path1) << endl;
}
