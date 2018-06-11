import pytest
from util import tsort


class TestTsort:

    def test_tsort(self):
        a = [(3, [8, 10]),
             (5, [11]),
             (11, [2, 9, 10]),
             (7, [8, 11]),
             (8, [9]),
             (10, [8]),
             ]
        result = tsort.tsort(a)
        assert result, ([3, 5, 7, 11, 10, 8, 2, 9], [])
