cmake_minimum_required(VERSION 3.3)
project(ai)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES ai.cpp game.cpp myai.cpp)
add_executable(ai ${SOURCE_FILES})
