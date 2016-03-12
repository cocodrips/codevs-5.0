cmake_minimum_required(VERSION 3.3)
project(ai)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES src/game.cpp src/point.cpp src/base.h src/cell.cpp src/character.cpp
        src/input.cpp  src/controller.h src/controller.cpp src/state.cpp src/brain.cpp src/point.h src/character.h
        src/state.h src/cell.h src/input.h src/direction.cpp src/direction.h src/output.cpp src/output.h src/brain.cpp
        src/brain.h src/path.cpp src/path.h src/evaluation.cpp src/evaluation.h)
add_executable(ai ${SOURCE_FILES})

set(SOURCE_FILES src/game.cpp)
add_executable(game ${SOURCE_FILES})

set(TEST_FILES src/point.cpp src/character.cpp
        src/cell.cpp gtest/cell_test.cpp src/input.cpp src/direction.cpp
        src/controller.cpp src/state.cpp src/output.cpp src/path.cpp src/brain.cpp src/evaluation.cpp
        gtest/point_test.cpp gtest/character_test.cpp gtest/input_test.cpp
        gtest/cell_test.cpp gtest/output_test.cpp gtest/path_test.cpp gtest/state_test.cpp
        gtest/brain_test.cpp)
include_directories(gtest)
link_directories(/Users/cocodrips/Documents/AI/codevs-5.0/ai/gtest)
add_executable(gtest ${TEST_FILES})
target_link_libraries(gtest libgtest.a libgtest_main.a)


