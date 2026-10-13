import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def api():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    return s


@pytest.fixture(scope="session")
def token(api):
    """Lấy token đăng nhập (tài khoản demo công khai của restful-booker)."""
    resp = api.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert resp.status_code == 200
    return resp.json()["token"]


@pytest.fixture
def booking_payload():
    return {
        "firstname": "Thuy",
        "lastname": "Ta",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def created_booking(api, booking_payload):
    """Tạo 1 booking làm dữ liệu test, trả về (id, payload)."""
    resp = api.post(f"{BASE_URL}/booking", json=booking_payload)
    assert resp.status_code == 200
    return resp.json()["bookingid"], booking_payload
