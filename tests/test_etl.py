from schemas.data import APIRecord


def test_api_record_validation():
    data = {
        "record_id": "1",
        "name": "Test Name",
        "value": "123"
    }

    record = APIRecord(**data)

    assert record.record_id == "1"
    assert record.name == "Test Name"
    assert record.value == "123"
