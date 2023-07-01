import pytest
import datetime
from project import get_city, get_unit, convert_unix


def test_get_city():
    with pytest.raises(ValueError):
        get_city("")
    with pytest.raises(ValueError):
        get_city("paris123#@$")
    assert get_city("london") == "london"


def test_get_unit():
    with pytest.raises(ValueError):
        get_unit("")
    with pytest.raises(ValueError):
        get_unit("E")
    with pytest.raises(ValueError):
        get_unit(234)
    assert get_unit("c") == "metric"
    assert get_unit("f") == "imperial"


def test_convert_unix():
    assert convert_unix(1688130000, 7200) == datetime.datetime(2023, 6, 30, 15, 0)
