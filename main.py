from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# CHAPTER 1: App config
# ---------------------------------------------------------
app = FastAPI(
    title="Coupon Validator (Tennis Store)",
    description="Lightweight REST API to validate promo codes and calculate cart discounts.",
    version="1.0.0",
)


# ---------------------------------------------------------
# CHAPTER 2: Bussines logic (also objects)
# ---------------------------------------------------------
class DiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"


class Coupon(BaseModel):
    code: str
    discount_type: DiscountType
    value: float
    active: bool


# ---------------------------------------------------------
# CHAPTER 3: Database
# ---------------------------------------------------------
COUPONS: dict[str, Coupon] = {
    "CUPON10": Coupon(
        code="CUPON10",
        discount_type=DiscountType.PERCENTAGE,
        value=10.0,
        active=True,
    ),
    "KICKS20": Coupon(
        code="KICKS20",
        discount_type=DiscountType.PERCENTAGE,
        value=20.0,
        active=True,
    ),
    "FIJO15": Coupon(
        code="FIJO15",
        discount_type=DiscountType.FIXED,
        value=15.0,
        active=True,
    ),
    "EXPIRED": Coupon(
        code="EXPIRED",
        discount_type=DiscountType.PERCENTAGE,
        value=50.0,
        active=False,
    ),
}

# ---------------------------------------------------------
# CHAPTER 4: Business logic
# ---------------------------------------------------------
INVALID_MESSAGE = "Invalid coupon"
SUCCESS_MESSAGE = "Coupon applied successfully!"


def _round_money(amount: float) -> float:
    return round(amount, 2)


def calculate_discount(coupon: Coupon, total_amount: float) -> float:
    if coupon.discount_type == DiscountType.PERCENTAGE:
        discount = total_amount * (coupon.value / 100.0)
    else:
        discount = coupon.value
    return _round_money(min(discount, total_amount))


# ---------------------------------------------------------
# CHAPTER 5: Controller (some objects)
# ---------------------------------------------------------
class CouponValidateRequest(BaseModel):
    code: str = Field(..., min_length=1, examples=["CUPON10"])
    totalAmount: float = Field(..., ge=0, examples=[100.0])


class CouponValidateResponse(BaseModel):
    valid: bool
    discount: float
    finalAmount: float
    message: str


def _invalid_response(total_amount: float) -> CouponValidateResponse:
    return CouponValidateResponse(
        valid=False,
        discount=0.0,
        finalAmount=_round_money(total_amount),
        message=INVALID_MESSAGE,
    )


# ---------------------------------------------------------
# CAPÍTULO 6: Controller and Endpoint
# ---------------------------------------------------------
@app.post("/api/coupons/validate", response_model=CouponValidateResponse)
def validate_coupon(payload: CouponValidateRequest) -> CouponValidateResponse:
    coupon = COUPONS.get(payload.code.strip().upper())

    if coupon is None or not coupon.active:
        return _invalid_response(payload.totalAmount)

    discount = calculate_discount(coupon, payload.totalAmount)
    final_amount = _round_money(payload.totalAmount - discount)

    return CouponValidateResponse(
        valid=True,
        discount=discount,
        finalAmount=final_amount,
        message=SUCCESS_MESSAGE,
    )
