#include <boost/python.hpp>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "RuleEngine.h"

using namespace std;
namespace bp = boost::python;

struct RuleEngine {
  RuleEngine(bp::dict const& facts, bp::dict const& rules)
    : engine{facts, rules}
  {}

  bp::tuple
  execute(bp::dict const& facts)
  {
    std::map<std::string, bool> fact_vals;

    auto fnames = facts.keys();
    for (int i = 0; i < len(fnames); ++i) {
      fact_vals.emplace(bp::extract<string>(fnames[i]),
                        bp::extract<bool>(facts[fnames[i]]));
    }

    std::map<std::string, std::vector<std::string>> out_actions;
    std::map<std::string, std::map<std::string, bool>> out_facts;

    engine.execute(fact_vals, out_actions, out_facts);

    bp::dict py_actions;
    bp::dict py_facts;

    for (auto const& act : out_actions) {
      bp::list act_names;
      for (auto const& act_name : act.second)
        act_names.append(act_name);

      py_actions[act.first] = act_names;
    }

    for (auto const& rule_facts : out_facts) {
      bp::dict py_rule_facts;
      for (auto const& fact_val : rule_facts.second)
        py_rule_facts[fact_val.first] = fact_val.second;

      py_facts[rule_facts.first] = py_rule_facts;
    }

    return bp::make_tuple(py_actions, py_facts);
  }

private:
  logic_engine::RuleEngine engine;
};

BOOST_PYTHON_MODULE(RE)
{
  bp::class_<RuleEngine, boost::noncopyable>(
    "RuleEngine", bp::init<bp::dict, bp::dict>())
    .def("execute", &RuleEngine::execute);
}
