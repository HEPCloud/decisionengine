import pytest

from decisionengine.framework.dataspace import dataspace

def test_dataspace_config_finds_bad():
    with pytest.raises(dataspace.DataSpaceConfigurationError) as e:
        dataspace.DataSpace({})
    assert e.match('missing dataspace information')

    with pytest.raises(dataspace.DataSpaceConfigurationError) as e:
        dataspace.DataSpace({'dataspace': 'asdf'})
    assert e.match('dataspace key must correspond to a dictionary')

    with pytest.raises(dataspace.DataSpaceConfigurationError) as e:
        dataspace.DataSpace({'dataspace': {'asdf': 'asdf'}})
    assert e.match('Invalid dataspace configuration')
