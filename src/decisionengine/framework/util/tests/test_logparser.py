# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import os
import re
import subprocess

import decisionengine.framework.util.logparser as logparser


# Unfortunately, because argparse short-circuits the '-h' process, we
# need to run the -h option as a separate process, capturing the
# output for testing.
def test_logparser_help():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    logparser_cmd = os.path.join(this_dir, "../logparser.py")
    output = subprocess.run([logparser_cmd, "-h"], stdout=subprocess.PIPE, universal_newlines=True).stdout
    assert re.match("usage", output) is not None
    # Optional arguments are called "options" in python 3.10 and "optional arguments" in 3.9 and earlier
    assert re.search("optional arguments:", output) is not None or re.search("options:", output) is not None
    assert re.search("positional arguments", output) is not None


def test_logparser_with_invalid_file():
    assert (
        logparser.main(["-f", "1", "./not_existing_file.txt"])
        == "An error occurred while trying to parse './not_existing_file.txt'\n"
        + "Please ensure that the log file name is correct."
    )


def test_logparser_with_invalid_file_verbose():
    output = logparser.main(["-v", "-f", "1", "./not_existing_file.txt"])
    assert output.startswith(
        " An error occurred while trying to parse './not_existing_file.txt'\n"
        "Please ensure that the log file name is correct."
    )
    assert "No such file or directory" in output


def test_logparser_with_no_fields_verbose():
    assert (
        logparser.main(["-v", "./not_existing_file.txt"])
        == " An error occurred while trying to parse './not_existing_file.txt'\n"
        + "Please ensure that you requested some fields or keys.\n"
        + "No field or key specified"
    )


def test_logparser_with_directory_no_fields_invalid_file():
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
    outmsg = logparser.console_scripts_main(["-e", fixtures_dir, "not_existing_file.txt"])
    assert outmsg is not None
    assert (
        outmsg
        == "An error occurred while trying to parse 'not_existing_file.txt'\n"
        + "Please ensure that you requested some fields or keys."
    )


def test_logparser_with_directory():
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
    assert logparser.console_scripts_main(["-e", fixtures_dir, "-v", "-f", "1", "log_sample.txt"]) is None


def test_logparser_with_directory_not_verbose():
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
    assert logparser.console_scripts_main(["-e", fixtures_dir, "-f", "1", "log_sample.txt"]) is None


def test_logparser_parse_constraints():
    assert logparser.parse_constraints(["3 INFO", "2 publisher", "logger channel"]) == {
        "fields": [(3, "INFO"), (2, "publisher")],
        "keys": [("logger", "channel")],
    }
    assert logparser.parse_constraints(["3 INFO"]) == logparser.parse_constraints(None, "INFO")
    assert logparser.parse_constraints(None) is None


def test_logparser_matches_constraint():
    linelist = ["2021-10-22 17:07:58,483", "channel", "publisher", "DEBUG"]
    linedict = {
        "channel": "resource_request",
        "class_module": "fe_group_classads",
        "event": "No glideclient classads found",
    }
    assert logparser.matches_constraint(None, linelist, linedict) is True
    assert logparser.matches_constraint({"fields": [(4, "DEBUG")], "keys": []}, linelist, linedict) is False
    assert logparser.matches_constraint({"fields": [], "keys": [("extra", "NotThere")]}, linelist, linedict) is False
    assert (
        logparser.matches_constraint({"fields": [(3, "INFO"), (2, "publisher")], "keys": []}, linelist, linedict)
        is False
    )
    assert (
        logparser.matches_constraint({"fields": [(3, "DEBUG"), (2, "publisher")], "keys": []}, linelist, linedict)
        is True
    )
    assert (
        logparser.matches_constraint(
            {"fields": [(3, "DEBUG")], "keys": [("channel", "resource_request")]}, linelist, linedict
        )
        is True
    )
    assert (
        logparser.matches_constraint({"fields": [], "keys": [("channel", "resource_request")]}, linelist, linedict)
        is True
    )
    assert logparser.matches_constraint({"fields": [], "keys": [("channel", "resource")]}, linelist, linedict) is False


def test_logparser_field():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    logtoparse = os.path.join(this_dir, "fixtures", "log_sample.txt")
    assert (
        logparser.main(["-d", "-f", "1,2", logtoparse])
        == """channel,fe_group_classads
channel,fe_group_classads
channel,fe_group_classads
channel,publisher
channel,glide_frontend_element
channel,glide_frontend_element
channel,glide_frontend_element
channel,glide_frontend_element
channel,glide_frontend_element
NOT_AVAILABLE,NOT_AVAILABLE"""
    )


def test_logparser_field_key_separators():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    logtoparse = os.path.join(this_dir, "fixtures", "log_sample.txt")
    assert (
        logparser.main(["-d", "-v", "-s", ";", "-i", "- ", "-f", "1,2", "-k", "level", logtoparse])
        == """channel ;fe_group_classads ;debug
channel ;fe_group_classads ;info
channel ;fe_group_classads ;info
channel ;publisher ;info
channel ;glide_frontend_element ;debug
channel ;glide_frontend_element ;info
channel ;glide_frontend_element ;info
channel ;glide_frontend_element ;info
channel ;glide_frontend_element ;NOT_AVAILABLE
NOT_AVAILABLE;NOT_AVAILABLE;info"""
    )


def test_logparser_key():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    logtoparse = os.path.join(this_dir, "fixtures", "log_sample.txt")
    assert (
        logparser.main(["-d", "-v", "-k", "event", logtoparse])
        == """in GlideinWMSManifests publish
Facts available in publisher GlideinWMSManifests: [{'rule_name': 'publish_aws_requests', 'fact_name': 'allow_aws_requests', 'fact_value': True}, {'rule_name': 'publish_gce_requests', 'fact_name': 'allow_gce_requests', 'fact_value': False}, {'rule_name': 'publish_grid_requests', 'fact_name': 'allow_grid_requests', 'fact_value': True}, {'rule_name': 'publish_lcf_requests', 'fact_name': 'allow_lcf_requests', 'fact_value': True}]
Setting ReqIdleGlideins=0 for fact: allow_gce_requests
No glideclient classads found to advertise
Finding fe slots matching condition: GLIDECLIENT_NAME.str.startswith("hep-example-com_hepcloud_decisionengine.")
Jobs found total 2 idle 2 (good 2, old(10min 2, 60min 2), grid 2, voms 2) running 0
Group slots found total 0 (limit 60000 curb 59000) idle 0 (limit 60000 curb 59000) running 0
Frontend slots found total 260 (limit 170000 curb 167000) idle 260 (limit 35000 curb 25000) running 0
NOT_AVAILABLE
Frontend slots found total 260 (limit 170000 curb 167000) idle 260 (limit 35000 curb 25000) running 0"""
    )


def test_logparser_field_constraint_key():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    logtoparse = os.path.join(this_dir, "fixtures", "log_sample.txt")
    assert (
        logparser.main(["-d", "-c", "2 publisher", "-k", "event", logtoparse])
        == "No glideclient classads found to advertise"
    )


def test_logparser_key_constraint_key():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    logtoparse = os.path.join(this_dir, "fixtures", "log_sample.txt")
    assert (
        logparser.main(["-d", "-c", "level debug", "-k", "event", logtoparse])
        == """in GlideinWMSManifests publish
Finding fe slots matching condition: GLIDECLIENT_NAME.str.startswith("hep-example-com_hepcloud_decisionengine.")"""
    )


def test_logparser_level_constraint_key():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    logtoparse = os.path.join(this_dir, "fixtures", "log_sample.txt")
    assert (
        logparser.main(["-d", "-l", "DEBUG", "-k", "event", logtoparse])
        == """in GlideinWMSManifests publish
Finding fe slots matching condition: GLIDECLIENT_NAME.str.startswith("hep-example-com_hepcloud_decisionengine.")"""
    )
