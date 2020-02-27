
cmake_minimum_required(VERSION 3.0)

project(logicengine)

set(logicengine_version_major 2)
set(logicengine_version_minor 0)

#set(CMAKE_CXX_FLAGS "-std=c++1y -DASIO_STANDALONE ${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS}")

#OpenSSL Libraries
find_package(Boost REQUIRED)
find_package(PythonLibs ${PYVER})

# for vim ycm plugin
set(CMAKE_EXPORT_COMPILE_COMMANDS "ON")

include_directories(
    ${PROJECT_SOURCE_DIR}
    ${PROJECT_SOURCE_DIR}/src
    ${PROJECT_SOURCE_DIR}/utils
    ${Boost_INCLUDE_DIRS}
    ${PYTHON_INCLUDE_DIRS}
)
#INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})

link_directories(
    ${PROJECT_SOURCE_DIR}/install/lib
)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

add_subdirectory(ErrorHandler)

add_custom_target(liblinks ln -s ${CMAKE_BINARY_DIR}/ErrorHandler/RE.so ${CMAKE_SOURCE_DIR}/../ COMMAND ln -s ${CMAKE_BINARY_DIR}/ErrorHandler/libLogicEngine.so ${CMAKE_SOURCE_DIR}/../)
