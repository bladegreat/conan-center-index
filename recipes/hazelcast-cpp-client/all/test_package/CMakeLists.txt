cmake_minimum_required(VERSION 3.10)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(hazelcastcxx REQUIRED)

add_executable(test_package test_package.cpp)
target_link_libraries(test_package PUBLIC hazelcastcxx::hazelcastcxx)
set_property(TARGET test_package PROPERTY CXX_STANDARD 11)
