#include "gtest/gtest.h"
#include "../src/controller.h"
#include "../src/point.h"
#include "../src/input.h"
#include "../src/cell.h"
#include "../src/state.h"
#include "../src/brain.h"
#include <fstream>

TEST(BrainTest, dog_step) {
    Controller controller = Controller();
    ifstream f("inputs/next_dog.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    State state = controller.myState;
    state.setStepsToNinjas();

    Brain::setNextDogs(&state);
    stringstream ss;
    state.dumpField(ss);
    EXPECT_EQ(ss.str(),
              "WWWWWWWWWWWWWW\n"
              "W    O       W\n"
              "W        xx  W\n"
              "W         xxxW\n"
              "W    O   1OOxW\n"
              "W O  O   O  xW\n"
              "W       O    W\n"
              "W   OOOOOOOO W\n"
              "W  OOOO  xOO W\n"
              "W    O   xxxxW\n"
              "W   OOOOOOOOxW\n"
              "W     OO  OOxW\n"
              "W       xxxxxW\n"
              "W O  O OxO   W\n"
              "W      O     W\n"
              "W            W\n"
              "WWWWWWWWWWWWWW\n");
}
