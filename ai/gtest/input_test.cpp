#include "gtest/gtest.h"
#include "../src/codevs.h"
#include "../src/input.h"
#include "../src/controller.h"
#include <fstream>

TEST(InputTest, set_field) {
    Controller controller = Controller();
    ifstream f("inputs/next_dog.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    stringstream ss;
    controller.myState.dumpField(ss);



//    EXPECT_EQ(ss.str(),
//            "WWWWWWWWWWWWWW\n"
//            "W    O       W\n"
//            "W         xx W\n"
//            "W          xxW\n"
//            "W    O   1OOxW\n"
//            "W O  O   O  xW\n"
//            "W       O   xW\n"
//            "W   OOOOOOOO W\n"
//            "W  OOOO  xOO W\n"
//            "W    O  xxxxxW\n"
//            "W   OOOOOOOOxW\n"
//            "W     OO  OOxW\n"
//            "W        2xxxW\n"
//            "W O  O OxO   W\n"
//            "W      Ox    W\n"
//            "W            W\n"
//            "WWWWWWWWWWWWWW\n");
}
