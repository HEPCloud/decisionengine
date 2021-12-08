# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# The functionality provided here supports the translation of one
# string to another using the syntax 'old -> new', subject to the
# following constraints:
#
#   - The 'old' and 'new' strings may contain the following
#     characters: a-z, A-Z, 0-9, and _ (underscore).
#
#   - If '->' is provided, it must be surrounded by at least one space
#     on either side.
#
# The behavior is the following:
#
#   - translate("old") == ("old", None)
#   - translate("old -> new") == ("old", "new")
#   - translate_all(["old", "old1 -> new1"]) == {"old": "old", "old1": "new1"}

import re


def translate(spec):
    """Break apart the string 'old -> new' into a tuple ('old', 'new')"""
    match = re.fullmatch(R"(\w+)(\s+\->\s+(\w+))?", spec)
    if match is None:
        raise RuntimeError(
            f"The specification '{spec}' does not match the supported pattern "
            '"old_name[ -> new_name]",\n'
            "where the product names can consist of the characters a-z, a-Z, 0-9, "
            "and an underscore '_'.\nIf an optional new name is specified, the '->' "
            "token must be surrounded by at least\none space on either side."
        )
    return match.group(1, 3)


def translate_all(specs):
    result = {}
    for entry in specs:
        old, new = translate(entry)
        if new is None:
            new = old
        result[old] = new
    return result
