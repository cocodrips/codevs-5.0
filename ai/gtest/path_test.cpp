#include "gtest/gtest.h"
#include "../src/codevs.h"
#include "../src/point.h"
#include "../src/path.h"


#include <fstream>

TEST(PathTest, path2_destination) {
    map<Point, vector<vector<Point>>> path2 = Path::destinations[2];
    EXPECT_EQ(path2[Point(0, 0)].size(), 5);
    EXPECT_EQ(path2[Point(-1, 1)].size(), 2);
}

TEST(PathTest, path_pattern) {
    for (vector<Point> path : Path::destinations[2].at(Point(0, 0))) {
        for (Point p : path) {
            cout << p.print() << " ";
        }
        cout << endl;
    }
}