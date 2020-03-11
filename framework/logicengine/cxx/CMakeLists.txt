cmake_minimum_required(VERSION 3.0)

project(logicengine)

set(logicengine_version_major 2)
set(logicengine_version_minor 0)

set(CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS} -pedantic -Wall")

find_package(PythonInterp ${PYVER} REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(Boost REQUIRED)

# for vim ycm plugin
set(CMAKE_EXPORT_COMPILE_COMMANDS "ON")

set(BOOST_PY_SUFFIX 3)
if(PYTHONLIBS_VERSION_STRING VERSION_LESS "3.0.0")
  set(BOOST_PY_SUFFIX)
endif()

add_subdirectory(ErrorHandler)

add_custom_target(liblinks ln -s ${CMAKE_BINARY_DIR}/ErrorHandler/RE.so ${CMAKE_SOURCE_DIR}/../ COMMAND ln -s ${CMAKE_BINARY_DIR}/ErrorHandler/libLogicEngine.so ${CMAKE_SOURCE_DIR}/../)
