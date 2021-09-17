import tempfile

from decisionengine.framework.engine.DecisionEngine import _get_global_config, parse_program_options

# Because we just want to ensure correct behavior of program options
# overriding a configuration, it is not necessary to have a valid DE
# server configuration.  We therefore produce a small, temporary file
# with the valid Jsonnet configuration '{}'.

global_config_file = tempfile.NamedTemporaryFile()
global_config_file.write(b"{}")
global_config_file.flush()

# We do not call the DE's _get_de_conf_manager as that assumes the
# presence of configuration directories, which are unnecessary for
# this test.
def _check_override(arguments):
    options = parse_program_options(arguments)
    return _get_global_config(global_config_file.name, options)


def test_default_config():
    arguments = []
    assert _check_override(arguments) == {"server_address": ["localhost", 8888]}


def test_change_port():
    arguments = ["--port=54321"]
    assert _check_override(arguments) == {"server_address": ["localhost", 54321]}
