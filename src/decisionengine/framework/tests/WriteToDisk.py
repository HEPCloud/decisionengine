# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

"""Special publisher used to register publish calls with an external file.

It is difficult to interact with individual publishers while testing a
workflow.  The WriteToDisk publisher therefore writes to an external
file that can be read by a test.  Ideally, we would implement a system
so that the test and any instance of the WriteToDisk class are passed
the same file-name string.  Unfortunately, this is non-trivial to
achieve without adjusting the behavior of the decision-engine server
itself.  We therefore choose the following abstruse logic:

- WriteToDisk creates a temporary file and broadcasts its name to
  STDOUT.  Note that this temporary file must be uniquely named as
  multiple tests can use WriteToDisk in parallel.

- Capture STDOUT in the DETestWorker class.

- Pass STDOUT to the 'wait_for_n_writes' which will wait until the
  number 'n' appears in the file.
"""

import re
import tempfile
import time

from typing import Any

from decisionengine.framework.modules import Publisher
from decisionengine.framework.modules.Publisher import Parameter


def wait_for_n_writes(stdout, n):
    match = re.search("WriteToDisk:(.*?):", stdout, re.DOTALL)
    assert match is not None
    with open(match.group(1)) as f:
        while True:
            lines = f.readlines()
            if lines and int(lines[-1].strip()) >= n:
                return
            time.sleep(1)


@Publisher.supports_config(Parameter("filename", type=str), Parameter("consumes", type=list))
class WriteToDisk(Publisher.Publisher):
    def __init__(self, config):
        super().__init__(config)
        # TODO: need method to clean up file eventually
        self.file = tempfile.NamedTemporaryFile("w")
        print(f"WriteToDisk:{self.file.name}:")
        self.counter = 0
        self._consumes = {key: Any for key in config["consumes"]}
        self.file.write(f"{self.counter}\n")
        self.file.flush()

    def publish(self, data_block):
        self.counter += 1
        self.file.write(f"{self.counter}\n")
        self.file.flush()


Publisher.describe(WriteToDisk)
