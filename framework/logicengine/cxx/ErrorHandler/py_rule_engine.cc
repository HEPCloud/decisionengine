#include <boost/python.hpp>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "ErrorHandler/ma_rule_engine.h"

using namespace std;
using namespace boost::python;

struct RuleEngine {
  RuleEngine(boost::python::dict const& facts, boost::python::dict const& rules)
    : engine{facts, rules}
  {}

  boost::python::tuple
  execute(boost::python::dict const& facts)
  {
    std::map<std::string, bool> fact_vals;

    auto fnames = facts.keys();
    for (int i = 0; i < len(fnames); ++i) {
      fact_vals.emplace(extract<string>(fnames[i]),
                        extract<bool>(facts[fnames[i]]));
    }

    std::map<std::string, std::vector<std::string>> out_actions;
    std::map<std::string, std::map<std::string, bool>> out_facts;

    engine.execute(fact_vals, out_actions, out_facts);

    dict py_actions;
    dict py_facts;

    for (auto const& act : out_actions) {
      boost::python::list act_names;
      for (auto const& act_name : act.second)
        act_names.append(act_name);

      py_actions[act.first] = act_names;
    }

    for (auto const& rule_facts : out_facts) {
      dict py_rule_facts;
      for (auto const& fact_val : rule_facts.second)
        py_rule_facts[fact_val.first] = fact_val.second;

      py_facts[rule_facts.first] = py_rule_facts;
    }

    return boost::python::make_tuple(py_actions, py_facts);
  }

private:
  novadaq::errorhandler::ma_rule_engine engine;
};

BOOST_PYTHON_MODULE(RE)
{
  class_<RuleEngine, boost::noncopyable>(
    "RuleEngine", init<boost::python::dict, boost::python::dict>())
    .def("execute", &RuleEngine::execute);
}
