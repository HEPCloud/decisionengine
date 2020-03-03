#include <fstream>
#include <iostream>

#include "ErrorHandler/json/json.h"
#include "ErrorHandler/ma_rule_engine.h"

int
main(int argc, char** argv)
{
  fhicl::ParameterSet conf;

  if (argc > 1) {
    std::ifstream in(argv[1], std::ifstream::binary);

    if (in.is_open()) {
      in >> conf;
      in.close();
    }
  }

  Json::StyledWriter writer;
  std::cout << writer.write(conf);

  novadaq::errorhandler::ma_rule_engine engine(
    conf["conditions"], conf["rules"]);

  std::map<std::string, bool> facts_vals;
  facts_vals.emplace("c1", false);
  facts_vals.emplace("c2", true);

  std::map<std::string, std::vector<std::string>> actions;
  std::map<std::string, std::map<std::string, bool>> facts;

  engine.execute(facts_vals, actions, facts);

  std::cout << "\n\n";
  std::cout << "triggered actions\n";

  for (auto const& action : actions) {
    std::cout << action.first << ": ";

    for (auto const& name : action.second) {
      std::cout << name << ", ";
    }

    std::cout << "\n";
  }

  std::cout << "intermediate facts\n";
  for (auto const& fact : facts) {
    std::cout << fact.first << ": ";

    for (auto const& fact_val : fact.second) {
      std::cout << fact_val.first << ": " << fact_val.second << ", ";
    }

    std::cout << "\n";
  }

  // execute another time
  actions.clear();
  facts.clear();

  engine.reset_rules();
  engine.execute(facts_vals, actions, facts);

  std::cout << "\n\n";
  std::cout << "triggered actions\n";

  for (auto const& action : actions) {
    std::cout << action.first << ": ";

    for (auto const& name : action.second) {
      std::cout << name << ", ";
    }

    std::cout << "\n";
  }

  std::cout << "intermediate facts\n";
  for (auto const& fact : facts) {
    std::cout << fact.first << ": ";

    for (auto const& fact_val : fact.second) {
      std::cout << fact_val.first << ": " << fact_val.second << ", ";
    }

    std::cout << "\n";
  }

  std::cout << "hello world\n";
  return 0;
}
