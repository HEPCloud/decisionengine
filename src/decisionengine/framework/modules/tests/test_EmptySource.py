# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

import pytest

from decisionengine.framework.modules.EmptySource import EmptySource, pd


def test_empty_source_structure():
    params = {"data_product_name": "empty_data", "channel_name": "test"}
    test_empty_source = EmptySource(params)

    assert test_empty_source.get_parameters() == {"data_product_name": "empty_data", "channel_name": "test"}
    assert test_empty_source.data_product_name == "empty_data"

    assert test_empty_source._produces == {test_empty_source.data_product_name: pd.DataFrame}

    key, df = test_empty_source.acquire().popitem()
    assert key == test_empty_source.data_product_name
    assert isinstance(df, pd.DataFrame)
    assert df.empty


def test_missing_data_product_name_not_supported():
    params = {"data_product_name": "", "channel_name": "test"}

    with pytest.raises(RuntimeError, match="No data_product_name found in configuration"):
        EmptySource(params)
