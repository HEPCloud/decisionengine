# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os
import re
import subprocess

import decisionengine.framework.engine.de_client as de_client


# Unfortunately, because argparse short-circuits the '-h' process, we
# need to run the -h option as a separate process, capturing the
# output for testing.
def test_client_help(capfd):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    de_client_cmd = os.path.join(this_dir, "../de_client.py")
    output = subprocess.run([de_client_cmd, "-h"], stdout=subprocess.PIPE, universal_newlines=True).stdout
    assert re.match("usage", output) is not None
    assert re.search("optional arguments", output) is not None
    assert re.search("Decision Engine server options", output) is not None
    assert re.search("Channel-specific options", output) is not None
    assert re.search("Product-specific options", output) is not None
    assert re.search("Database reaper options", output) is not None


def test_client_with_no_server():
    assert (
        de_client.main(["--status"])
        == "An error occurred while trying to access a DE server at 'http://localhost:8888'\n"
        + "Please ensure that the host and port names correspond to a running DE instance."
    )


def test_client_with_no_command_says_use_help():
    # --verbose doesn't do anything without an action item
    msg = de_client.main(["--verbose"])
    if "-h" not in msg:
        raise ValueError(msg)


def test_client_with_no_server_verbose():
    msg = de_client.main(["--status", "--verbose"])
    if (
        "Connection refused" not in msg
        and "Cannot assign requested address" not in msg
        and "Network is unreachable" not in msg
    ):
        raise ValueError(msg)


def test_exclusive_options():
    assert de_client.main(["--force"]) == "The --force (-f) option may be used only with --kill-channel."
    assert (
        de_client.main(["--timeout", "2"])
        == "The --timeout option may be used only with --kill-channel or --block-while."
    )


def test_client_err_returned_as_rc():
    """no de server is running, so --status should error"""
    msg = de_client.console_scripts_main(["--status"])
    assert "An error occurred" in msg


def test_client_err_returned_verbose_as_rc():
    """no de server is running, so --status should error"""
    msg = de_client.console_scripts_main(["--status", "--verbose"])
    assert "An error occurred" in msg
