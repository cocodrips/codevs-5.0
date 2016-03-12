#include "gtest/gtest.h"
#include "../src/point.h"

TEST(PointTest, equal) {
    Point p1 = Point(1, 1);
    Point p2 = Point(1, 1);
    EXPECT_EQ(p1, p2);
}

TEST(PointTest, not_equal) {
    Point p1 = Point(1, 1);
    Point p2 = Point(1, 2);
    EXPECT_NE(p1, p2);
}

TEST(PointTest, print) {
    Point p1 = Point(1, 1);
    EXPECT_EQ(p1.print(), "P(1, 1)");
}