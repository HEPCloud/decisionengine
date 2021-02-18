cmake_minimum_required(VERSION 3.0)

project(logicengine LANGUAGES CXX)

set(logicengine_version_major 3)
set(logicengine_version_minor 0)

set(CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS} -pedantic -Wall -g -O3")

find_package(PythonInterp ${PYVER} REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(Boost REQUIRED)
find_package(pybind11 REQUIRED)

# for vim ycm plugin
set(CMAKE_EXPORT_COMPILE_COMMANDS "ON")

# python is starting to look at versioned .so suffix
execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/abisuffix.py OUTPUT_VARIABLE EXT_SUFFIX)
message(STATUS "Python suffix detected: '${EXT_SUFFIX}'")

pybind11_add_module(RE
    MODULE
    NO_EXTRAS
    ma_boolean_andexpr.cpp
    ma_boolean_cond.cpp
    ma_boolean_expr.cpp
    ma_parse.cpp
    Rule.cpp
    RuleEngine.cpp
    py_rule_engine.cc
)

target_include_directories(RE PRIVATE ${PYTHON_INCLUDE_DIRS} pybind11::headers)
target_link_libraries(RE PRIVATE pybind11::module pybind11::embed)
set_target_properties(RE PROPERTIES SUFFIX ${EXT_SUFFIX})

# Install in decisionengine/framework/logicengine subdirectory for
# Python runtime availability
install(TARGETS RE DESTINATION ${CMAKE_SOURCE_DIR}/../)
