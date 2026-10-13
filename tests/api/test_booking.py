import pytest
from jsonschema import validate

from tests.api.conftest import BASE_URL

pytestmark = pytest.mark.api

BOOKING_SCHEMA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
            },
        },
        "additionalneeds": {"type": "string"},
    },
}


def test_health_check(api):
    resp = api.get(f"{BASE_URL}/ping")
    assert resp.status_code == 201


def test_create_booking_returns_id_and_same_data(api, booking_payload):
    resp = api.post(f"{BASE_URL}/booking", json=booking_payload)
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body["bookingid"], int)
    assert body["booking"] == booking_payload


def test_get_booking_matches_schema(api, created_booking):
    booking_id, payload = created_booking
    resp = api.get(f"{BASE_URL}/booking/{booking_id}")
    assert resp.status_code == 200
    body = resp.json()
    validate(instance=body, schema=BOOKING_SCHEMA)
    assert body["totalprice"] == payload["totalprice"]


def test_update_booking_with_token(api, token, created_booking):
    booking_id, payload = created_booking
    updated = {**payload, "totalprice": 200, "additionalneeds": "Dinner"}
    resp = api.put(
        f"{BASE_URL}/booking/{booking_id}", json=updated, cookies={"token": token}
    )
    assert resp.status_code == 200
    assert resp.json()["totalprice"] == 200


def test_update_booking_without_token_is_forbidden(api, created_booking):
    booking_id, payload = created_booking
    resp = api.put(f"{BASE_URL}/booking/{booking_id}", json=payload)
    assert resp.status_code == 403


def test_delete_booking_then_not_found(api, token, created_booking):
    booking_id, _ = created_booking
    resp = api.delete(f"{BASE_URL}/booking/{booking_id}", cookies={"token": token})
    assert resp.status_code == 201

    resp = api.get(f"{BASE_URL}/booking/{booking_id}")
    assert resp.status_code == 404


def test_auth_with_wrong_password_returns_no_token(api):
    resp = api.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "wrong"})
    # restful-booker trả 200 kèm lý do lỗi, không trả token
    assert resp.status_code == 200
    assert "token" not in resp.json()
