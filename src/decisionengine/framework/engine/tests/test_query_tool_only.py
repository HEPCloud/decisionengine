import decisionengine.framework.engine.de_query_tool as de_query_tool

import re
import subprocess

# Unfortunately, because argparse short-circuits the '-h' process, we
# need to run the -h option as a separate process, capturing the
# output for testing.
def test_query_tool_help():
    de_query_tool_cmd = de_query_tool.__file__
    output = subprocess.run([de_query_tool_cmd, "-h"], stdout=subprocess.PIPE)
    assert re.match(b"usage: de_query_tool.py.*"
                    b"positional arguments.*"
                    b"optional arguments.*",
                    output.stdout,
                    flags=re.DOTALL)

def test_query_tool_with_no_server():
    assert de_query_tool.main(['foo']) == \
        "An error occurred while trying to access a DE server at 'http://localhost:8888'\n" + \
        "Please ensure that the host and port names correspond to a running DE instance."

def test_query_tool_with_no_server_verbose():
    msg = de_query_tool.main(['foo', '--verbose'])
    if "Connection refused" not in msg \
            and "Cannot assign requested address" not in msg \
            and "Network is unreachable" not in msg:
        raise ValueError(msg)
