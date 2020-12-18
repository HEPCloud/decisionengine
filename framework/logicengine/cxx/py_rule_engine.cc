#include <pybind11/pybind11.h>

#include <map>
#include <string>
#include <vector>

#include "RuleEngine.h"

using namespace std;
namespace py = pybind11;

struct RuleEngine {
  RuleEngine(py::dict const& facts, py::dict const& rules)
    : engine{facts, rules}
  {}

  py::tuple
  execute(py::dict const& facts)
  {
    std::map<std::string, bool> fact_vals;

    for (auto const& pr : facts) {
      fact_vals.emplace(py::cast<string>(pr.first),
                        py::cast<bool>(pr.second));
    }

    std::map<std::string, std::vector<std::string>> out_actions;
    std::map<std::string, std::map<std::string, bool>> out_facts;

    engine.execute(std::make_pair(std::string{}, fact_vals),
                   out_actions,
                   out_facts);

    py::dict py_actions;
    py::dict py_facts;

    for (auto const& act : out_actions) {
      py::list act_names;
      for (auto const& act_name : act.second)
        act_names.append(act_name);

      py_actions[act.first.c_str()] = act_names;
    }

    for (auto const& rule_facts : out_facts) {
      py::dict py_rule_facts;
      for (auto const& fact_val : rule_facts.second)
        py_rule_facts[fact_val.first.c_str()] = fact_val.second;

      py_facts[rule_facts.first.c_str()] = py_rule_facts;
    }

    return py::make_tuple(py_actions, py_facts);
  }

private:
  logic_engine::RuleEngine engine;
};

PYBIND11_MODULE(RE, m)
{
  py::class_<RuleEngine>(m, "RuleEngine")
    .def(py::init<py::dict, py::dict>())
    .def("execute", &RuleEngine::execute);
}
