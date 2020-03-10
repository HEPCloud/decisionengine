include_directories(
    ${PROJECT_SOURCE_DIR}
    ${Boost_INCLUDE_DIRS}
    ${PYTHON_INCLUDE_DIRS}
)

add_library(LogicEngine SHARED
    jsoncpp.cc
    ma_boolean_andexpr.cpp
    ma_boolean_cond.cpp
    ma_boolean_expr.cpp
    ma_cell.cpp
    Fact.cpp
    ma_hitmap.cpp
    ma_parse.cpp
    ma_rule.cpp
    ma_rule_engine.cpp
)
target_link_libraries(LogicEngine boost_regex)

python_add_module(RE py_rule_engine.cc)
target_link_libraries(RE LogicEngine boost_python boost_regex boost_system ${PYTHON_LIBRARIES})
