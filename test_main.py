from fastapi.testclient import TestClient
from main import app, INVALID_MESSAGE, SUCCESS_MESSAGE

# Initialize the FastAPI test client
client = TestClient(app)


def test_validate_percentage_coupon_success():
    """Verify that a percentage-based coupon (CUPON10) is applied correctly."""
    payload = {"code": "CUPON10", "totalAmount": 100.0}
    response = client.post("/api/coupons/validate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["discount"] == 10.0
    assert data["finalAmount"] == 90.0
    assert data["message"] == SUCCESS_MESSAGE


def test_validate_fixed_coupon_success():
    """Verify that a fixed-amount coupon (FIJO15) is applied correctly (case-insensitive)."""
    payload = {"code": "fijo15", "totalAmount": 50.0}
    response = client.post("/api/coupons/validate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["discount"] == 15.0
    assert data["finalAmount"] == 35.0


def test_validate_coupon_expired():
    """Verify that an inactive or expired coupon (EXPIRED) is rejected."""
    payload = {"code": "EXPIRED", "totalAmount": 100.0}
    response = client.post("/api/coupons/validate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["discount"] == 0.0
    assert data["finalAmount"] == 100.0
    assert data["message"] == INVALID_MESSAGE


def test_validate_coupon_not_found():
    """Verify that a non-existent coupon code is rejected."""
    payload = {"code": "NON_EXISTENT", "totalAmount": 100.0}
    response = client.post("/api/coupons/validate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["discount"] == 0.0


def test_discount_does_not_exceed_total_amount():
    """Verify edge case where a fixed discount exceeds the cart's total amount."""
    # FIJO15 grants $15 off, but the cart total is only $10
    payload = {"code": "FIJO15", "totalAmount": 10.0}
    response = client.post("/api/coupons/validate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["discount"] == 10.0  # Discount is capped at totalAmount
    assert data["finalAmount"] == 0.0  # Prevents negative final amounts
