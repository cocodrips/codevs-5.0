#include "gtest/gtest.h"
#include "../src/output.h"
#include "../src/controller.h"
#include "../src/point.h"
#include <fstream>

TEST(OutputTest, output_no_skill) {
    Controller controller = Controller();
    controller.myState.nextStep[0].push_back(Point(1, 0));
    controller.myState.nextStep[0].push_back(Point(0, 1));
    stringstream ss;

}
