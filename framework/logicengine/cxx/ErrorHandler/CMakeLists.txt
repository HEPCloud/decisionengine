
add_library(LogicEngine SHARED
    jsoncpp.cc
    ma_action.cpp
    ma_boolean_andexpr.cpp
    ma_boolean_cond.cpp
    ma_boolean_expr.cpp
    ma_cell.cpp
    ma_cond_test_andexpr.cpp
    ma_cond_test_expr.cpp
    ma_cond_test_primary.cpp
    ma_condition.cpp
    ma_domain_andexpr.cpp
    ma_domain_cond.cpp
    ma_domain_expr.cpp
    ma_function.cpp
    ma_function_count.cpp
    ma_function_countpercent.cpp
    ma_function_is_syncd.cpp
    ma_hitmap.cpp
    ma_parse.cpp
    ma_participants.cpp
    ma_richmsg.cpp
    ma_rule.cpp
    ma_rule_engine.cpp
    ma_test_function.cpp
    ma_utils.cpp
)

add_executable(test_main test_main.cc)
target_link_libraries(test_main LogicEngine boost_regex boost_system)

python_add_module(RE py_rule_engine.cc)
target_link_libraries(RE LogicEngine boost_python boost_regex boost_system ${PYTHON_LIBRARIES})
