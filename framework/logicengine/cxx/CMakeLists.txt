cmake_minimum_required(VERSION 3.0)

project(logicengine)

set(logicengine_version_major 2)
set(logicengine_version_minor 0)

set(CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS} -pedantic -Wall -g -O3")

find_package(PythonInterp ${PYVER} REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(Boost REQUIRED)

# for vim ycm plugin
set(CMAKE_EXPORT_COMPILE_COMMANDS "ON")

set(BOOST_PY_SUFFIX 3)
if(PYTHONLIBS_VERSION_STRING VERSION_LESS "3.0.0")
  set(BOOST_PY_SUFFIX)
endif()

include_directories(
    ${PROJECT_SOURCE_DIR}
    ${Boost_INCLUDE_DIRS}
    ${PYTHON_INCLUDE_DIRS}
)

add_library(LogicEngine SHARED
    ma_boolean_andexpr.cpp
    ma_boolean_cond.cpp
    ma_boolean_expr.cpp
    ma_parse.cpp
    Rule.cpp
    RuleEngine.cpp
)
target_link_libraries(LogicEngine boost_regex)

python_add_module(RE py_rule_engine.cc)
target_link_libraries(RE LogicEngine
                      boost_python${BOOST_PY_SUFFIX}
                      boost_system
                      ${PYTHON_LIBRARIES})

add_custom_target(liblinks ln -s ${CMAKE_BINARY_DIR}/RE.so ${CMAKE_SOURCE_DIR}/../ COMMAND ln -s ${CMAKE_BINARY_DIR}/libLogicEngine.so ${CMAKE_SOURCE_DIR}/../)
