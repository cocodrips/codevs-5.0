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
}

TEST(BrainTest,can_move_block) {
    Controller controller = Controller();
    ifstream f("inputs/near_block.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    State state = controller.myState;
    Point direction = Point(-1, 0);
    EXPECT_TRUE(Brain::canMove(state, state.ninjas[1].point, direction));
    state.ninjas[1].point = Brain::move(&state, state.ninjas[1].point, direction);

    EXPECT_FALSE(Brain::canMove(state, state.ninjas[1].point, direction));

//    state.setStepsToNinjas();
//    state.dumpField(cout);
}


TEST(BrainTest,move_to_destination) {
    Controller controller = Controller();
    ifstream f("inputs/block_escape.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    State state = controller.myState;

    Point me = state.ninjas[0].point;
    vector<Point> path(2);
    path[0] = Point(1, 0);
    path[1] = Point(1, 0);

    vector<Point> getSouls;
    set<Point> souls;
    int score = Brain::moveToDestination(&state, &me, path, &getSouls, souls);
    state.ninjas[0].point = me;

    state.setStepsToNinjas();
    state.dumpField(cout);
    EXPECT_TRUE(score > -INF);
}

TEST(BrainTest, pinch_doppel) {
    Controller controller = Controller();
    ifstream f("inputs/pinch_doppel.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    State state = controller.myState;

    state.dumpField(cout);

//    Point me = state.ninjas[0].point;
//    vector<Point> path(2);
//    path[0] = Point(1, 0);
//    path[1] = Point(1, 0);
//
//    vector<Point> getSouls;
//    set<Point> souls;
//    int score = Brain::moveToDestination(&state, &me, path, &getSouls, souls);
//    state.ninjas[0].point = me;
//
//    state.setStepsToNinjas();
//    state.dumpField(cout);
//    EXPECT_TRUE(score > -INF);
}
