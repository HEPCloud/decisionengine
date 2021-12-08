# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os
import re
import subprocess
import sys
import tempfile

import decisionengine


def _run_as_main(name, *program_options):
    my_env = os.environ.copy()
    de_path = os.path.dirname(os.path.dirname(decisionengine.__file__))
    if "PYTHONPATH" in my_env:
        my_env["PYTHONPATH"] = f"{my_env['PYTHONPATH']}:{de_path}"
    else:
        my_env["PYTHONPATH"] = de_path

    rc = subprocess.run(
        [sys.executable, "-m", "decisionengine.framework.tests." + name, *program_options],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=my_env,
    )
    return rc.returncode, rc.stdout.strip(), rc.stderr.strip()


def _normalize(string):
    # Replace multiple whitespaces with one whitespace
    return " ".join(string.split())


class Help:
    def __init__(self, name):
        self.name = name

    def test(self, has_sample_config=False):
        rc, stdout, _ = _run_as_main(self.name, "--help")
        assert rc == 0

        simple_stdout = _normalize(stdout).replace("optional arguments:", "options:")
        assert simple_stdout

        if "Source" in self.name:
            check_text = _expected_source_help(self.name, has_sample_config)
        else:
            check_text = _expected_help(self.name)

        assert simple_stdout == check_text


def _expected_help(name):
    help_msg = (
        f"usage: {name}.py [-h] [--describe] [--config-template] "
        + "options:"
        + "  -h, --help         show this help message and exit"
        + "  --describe         print config. template along with produces and consumes"
        + "                     information"
        + "  --config-template  print the expected module configuration"
    )
    return _normalize(help_msg)


def _expected_source_help(name, has_sample_config=False):
    help_msg = f"usage: {name}.py [-h] [--describe] [--config-template] [-c <channel config. file>] "
    if has_sample_config:
        help_msg += "[-s] "
    help_msg += """options:
  -h, --help            show this help message and exit
  --describe            print config. template along with produces and
                        consumes information
  --config-template  print the expected module configuration
  -c <channel config. file>, --acquire-with-config <channel config. file>
                        run the 'acquire' method of the source as configured
                        in the 'sources' block of the full channel
                        configuration """
    if has_sample_config:
        help_msg += """-s, --acquire-with-sample-config
                        run the 'acquire' method using the default
                        configuration provided by the module"""

    return _normalize(help_msg)


class ConfigTemplate:
    def __init__(self, name):
        self.name = name

    def test(self, has_comments=False):
        rc, stdout, _ = _run_as_main(self.name, "--config-template")
        assert rc == 0
        if has_comments:
            assert _normalize(stdout) == _expected_config_template_with_comments(self.name)
        else:
            assert stdout == _expected_config_template(self.name)


def _expected_config_template(name):
    return (
        "Supported channel configuration:\n\n"
        + "  <module name>: {\n"
        + f"    module: 'decisionengine.framework.tests.{name}',\n"
        + f"    name: '{name}',  # optional - can be inferred by framework\n"
        + "    parameters: {\n"
        + "    }\n"
        + "  }"
    )


def _expected_config_template_with_comments(name):
    printout = """Supported channel configuration:

  <module name>: {
    module: 'decisionengine.framework.tests.SupportsConfigPublisher',
    name: 'SupportsConfig',  # optional - can be inferred by framework
    parameters: {
      no_type: <type 'unknown'>,
      only_type: <type 'int'>,
      default_only: 2.5,  # default value
      convert_to: 3,  # default value
      comment: <type 'str'>,
      comment_with_nl: <type 'str'>,
    }
  }

where

  default_only (type 'float')
  convert_to (type 'int')
  comment (type 'str') - Single-line comment
  comment_with_nl (type 'str')

    Comment with newline"""
    return _normalize(printout)


class Describe:
    def __init__(self, name):
        self.name = name

    def test(self, consumes=None, produces=None):
        rc, stdout, _ = _run_as_main(self.name, "--describe")
        assert rc == 0
        description = ""
        if consumes:
            description += f"The following products are consumed:\n\n - {consumes} (type 'DataFrame')\n\n\n"
        if produces:
            description += f"The following products are produced:\n\n - {produces} (type 'DataFrame')\n\n\n"
        description += _expected_config_template(self.name)
        assert stdout == description


class DescribeAlias:
    def __init__(self, alias, original):
        self.alias = alias
        self.original = original

    def test(self):
        alias_rc, alias_stdout, _ = _run_as_main(self.alias, "--describe")
        orig_rc, orig_stdout, _ = _run_as_main(self.original, "--describe")
        assert alias_rc == 0
        assert orig_rc == 0
        assert _normalize(alias_stdout) == _normalize(orig_stdout)


class AcquireWithConfig:
    def __init__(self, name):
        self.name = name

    def test(self, byte_str, expected_stderr=""):
        with tempfile.NamedTemporaryFile(suffix=".jsonnet") as config_file:
            config_file.write(byte_str)
            config_file.flush()
            config_file.seek(0)
            rc, stdout, stderr = _run_as_main(self.name, "--acquire-with-config", config_file.name)
            if expected_stderr:
                assert rc == 1
                assert re.search(expected_stderr, _normalize(stderr), re.DOTALL)
            else:
                assert rc == 0
                assert _normalize(stdout) == _expected_acquire_result(self.name, config_file, 2, "test")


def _expected_acquire_result(name, config_file=None, multiplier=1, channel_name="test1"):
    result = ""
    if config_file is None:
        result += f"Running acquire for source {name} using default configuration:"
    else:
        result += f"Running acquire for source {name} using configuration from {config_file.name}:"
    result += (
        " {'channel_name': "
        + f"'{channel_name}'"
        + ", 'multiplier':  "
        + f"{multiplier}"
        + "} Produced products: {'foo':      col1  col2 "
        + f"0  value1   {0.5 * multiplier} "
        + f"1  value2   {2.0 * multiplier}"
        + "}"
    )
    return _normalize(result)


class AcquireWithSampleConfig:
    def __init__(self, name):
        self.name = name

    def test(self):
        rc, stdout, _ = _run_as_main(self.name, "--acquire-with-sample-config")
        assert rc == 0
        assert _normalize(stdout) == _expected_acquire_result(self.name)
