#include "gtest/gtest.h"
#include "../src/controller.h"
#include "../src/point.h"
#include "../src/input.h"
#include "../src/cell.h"
#include "../src/state.h"
#include <fstream>

TEST(StateTest, copy) {
    Controller controller = Controller();
    ifstream f("inputs/next_dog.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    State state = controller.myState;
    state.field[0][0] = Cell('8');

    EXPECT_NE(state.field[0][0].type, controller.myState.field[0][0].type);
}

TEST(StateTest, steps_from_point) {
    Controller controller = Controller();
    ifstream f("inputs/next_dog.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);

    stringstream ss;
    vector<Point> ninjas;
    ninjas.push_back(controller.myState.ninjas[0].point);
    ninjas.push_back(controller.myState.ninjas[1].point);
    auto steps = controller.myState.stepsFromPoints(ninjas);
    REP(y, Y) {
        REP(x, X) {
            ss << setw(2);

            if (steps[y][x] == INF) {
                ss << "__";
            } else {
                ss << steps[y][x];
            }
            ss << " ";

        }
        ss << endl;
    }
    EXPECT_EQ(ss.str(),
              "__ __ __ __ __ __ __ __ __ __ __ __ __ __ \n"
                      "__ 11 10  9  8 __  6  5  4  3  4  5  6 __ \n"
                      "__ 10  9  8  7  6  5  4  3  2  3  4  5 __ \n"
                      "__  9  8  7  6  5  4  3  2  1  2  3  4 __ \n"
                      "__ 10  9  8  7 __  3  2  1  0 __ __  5 __ \n"
                      "__ 11 __  9  8 __  4  3  2 __  8  7  6 __ \n"
                      "__ 10  9  8  7  6  5  4 __ 10  9  8  7 __ \n"
                      "__ 11 10  9 __ __ __ __ __ __ __ __  8 __ \n"
                      "__ 12 11 __ __ __ __ 12 11 10 __ __  7 __ \n"
                      "__ 11 10  9 10 __ 12 11 10  9  8  7  6 __ \n"
                      "__ 10  9  8 __ __ __ __ __ __ __ __  5 __ \n"
                      "__  9  8  7  6  5 __ __  2  1 __ __  4 __ \n"
                      "__  8  7  6  5  4  3  2  1  0  1  2  3 __ \n"
                      "__  9 __  7  6 __  4 __  2 __  2  3  4 __ \n"
                      "__ 10  9  8  7  6  5 __  3  4  3  4  5 __ \n"
                      "__ 11 10  9  8  7  6  5  4  5  4  5  6 __ \n"
                      "__ __ __ __ __ __ __ __ __ __ __ __ __ __ \n");

}

TEST(StateTest, steps_to_reachable_cell) {
    Controller controller = Controller();
    ifstream f("inputs/closed_sample.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    controller.myState.setStepsToReachableCellFromNinja();

    auto steps = controller.myState.stepsToReachableCellNinjas;
    stringstream ss;
    REP(y, Y) {
        REP(x, X) {
            ss << setw(2);

            if (steps[y][x] == INF) {
                ss << "__";
            } else {
                ss << steps[y][x];
            }
            ss << " ";

        }
        ss << endl;
    }
    cout << ss.str() << endl;
    EXPECT_EQ(ss.str(),
              "__ __ __ __ __ __ __ __ __ __ __ __ __ __ \n"
              "__ 15 14 13 14 15 __  5  4  3  2  1  2 __ \n"
              "__ 14 13 12 13 14 __ __ __ __ __  0  1 __ \n"
              "__ __ 12 11 12 13 14 15 16 __ __  1  2 __ \n"
              "__ 12 11 10 11 __ __ __ __ __ __ __ __ __ \n"
              "__ 11 10  9 10 __ __ __ __ __ __ __ __ __ \n"
              "__ 10  9  8 __ 16 17 14 13 __ __ __ __ __ \n"
              "__  9  8  7 __ 15 14 13 12 13 14 15 16 __ \n"
              "__  8  7  6 __ __ __ __ 11 12 13 16 15 __ \n"
              "__  7  6  5 __ __ __ __ 10 11 12 13 14 __ \n"
              "__  6  5  4 __ __  7  8  9 14 13 14 15 __ \n"
              "__  5  4  3 __  5  6 __ __ __ 12 13 14 __ \n"
              "__  4  3  2  3  4  5  6 __ __ 11 12 13 __ \n"
              "__  3  2  1  2  3  4  5 __ __ 10 11 12 __ \n"
              "__  2  1  0  1  2  3  6 __ __  9 10 11 __ \n"
              "__  3  2  1  2  3  4  5  6  7  8  9 10 __ \n"
              "__ __ __ __ __ __ __ __ __ __ __ __ __ __ \n");

}