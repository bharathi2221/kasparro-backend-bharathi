import pytest
from schemas.data import APIRecord


def test_invalid_api_record():
    bad_data = {
        "record_id": "1",
        # name missing
        "value": "123"
    }

    with pytest.raises(Exception):
        APIRecord(**bad_data)
