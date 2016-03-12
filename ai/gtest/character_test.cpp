#include "gtest/gtest.h"
#include "../src/character.h"

TEST(CharacterTest, equal) {
    Character chr = Character(1, 4, 6);
    Character chr2 = Character(2, 4, 6);

    EXPECT_TRUE(chr == chr2);
}
