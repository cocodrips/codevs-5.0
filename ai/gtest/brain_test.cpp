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

TEST(BrainTest, can_move_block) {
    Controller controller = Controller();
    ifstream f("inputs/near_block.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    State state = controller.myState;
    Point direction = Point(-1, 0);
    EXPECT_TRUE(Brain::canMove(state, state.ninjas[1].point, direction));
    state.ninjas[1].point = Brain::move(&state, state.ninjas[1].point, direction);

    EXPECT_FALSE(Brain::canMove(state, state.ninjas[1].point, direction));

}


TEST(BrainTest, move_to_destination) {
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
//    state.dumpField(cout);
    EXPECT_TRUE(score > -INF);
}

TEST(BrainTest, pinch_doppel) {
    Controller controller = Controller();
    ifstream f("inputs/pinch_doppel.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);
    State state = controller.myState;

}


TEST(BrainTest, closed_direction_num) {
    Controller controller = Controller();
    ifstream f("inputs/4closed_pos.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);

    State state = controller.myState;
    int num0 = Brain::closedDirectionNum(state, state.ninjas[0].point);
    int num1 = Brain::closedDirectionNum(state, state.ninjas[1].point);
    cout << "== " << num0 << " " << num1 << endl;
//    EXPECT_EQ(num0, 1);
//    EXPECT_EQ(num1, 3);

}

TEST(BrainTest, around_dog_num) {
    Controller controller = Controller();
    ifstream f("inputs/around_dog.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);

    State state = controller.myState;
    int num0 = Brain::aroundDogNum(state, state.ninjas[0].point);
    int num1 = Brain::aroundDogNum(state, state.ninjas[1].point);
    EXPECT_EQ(num0, 4);
    EXPECT_EQ(num1, 1);

}

TEST(BrainTest, senf_dog_test) {
    Controller controller = Controller();
    ifstream f("inputs/send_dog_test.txt");
    ASSERT_FALSE(f.fail());
    Input::mainInput(&controller, f);

    State state = controller.myState;
    vector<Point> path0;
    vector<Point> path1;
    state.dumpField(cerr);
    int defaultScore = Brain::setBestPath(state, 2, &path0, &path1, -INF);

    state.dogPoints.clear();
    state.dogs.clear();
    state.dumpField(cerr);
    int score = Brain::setBestPath(state, 2, &path0, &path1, -INF);

}