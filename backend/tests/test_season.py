import pytest
from app.domain.season import parse_season

def test_2026_27():
    assert parse_season("2026-27").provider_year == 2026

@pytest.mark.parametrize("value", ["2026", "26-27", "2026-28", "bad"])
def test_invalid(value):
    with pytest.raises(ValueError):
        parse_season(value)
