# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest

from decisionengine.framework.modules.translate_product_name import translate, translate_all


def test_translate_none():
    with pytest.raises(RuntimeError, match="does not match the supported pattern"):
        translate("")
    assert translate("old") == ("old", None)


def test_translate_simple():
    assert translate("old -> new") == ("old", "new")


def test_translate_with_underscores():
    assert translate("old_v0 -> new_v1") == ("old_v0", "new_v1")


def test_translate_illegal_characters():
    with pytest.raises(RuntimeError, match="does not match the supported pattern"):
        translate("old-v0 -> new-v1")
    with pytest.raises(RuntimeError, match="does not match the supported pattern"):
        translate("old-<3=->=new-<3")


def test_translate_all():
    specs = ["old", "old1 -> new1"]
    assert translate_all(specs) == {"old": "old", "old1": "new1"}
