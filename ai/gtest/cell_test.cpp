#include "gtest/gtest.h"
#include "../src/cell.h"

TEST(CellTest, equal) {
    Cell c = Cell('W');
    EXPECT_EQ(c.isWall(), true);
    EXPECT_EQ(c.isEmpty(), false);

    Cell block = Cell('O');
    EXPECT_EQ(block.isBlock(), true);
    EXPECT_EQ(block.isEmpty(), false);
}
