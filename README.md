# FastAPI Coupon Validator (Tennis Store)

A lightweight REST API microservice built with **Python 3.11+** and **FastAPI** to validate e-commerce promo codes and calculate cart discounts in real time.

There is no external database setup required. Four sample coupons live in a dictionary in memory. The service automatically checks if a coupon exists, verifies its active status, and applies either a percentage or a fixed discount.

## Technical Features

- **Case-Insensitive Lookup:** Coupon codes are checked regardless of casing (e.g. `cupon10` matches `CUPON10`).
- **Edge-Case Validation:** Business logic guarantees that the discount value never exceeds `totalAmount`.
- **Zero Database Overhead:** Runs entirely in memory using a Python `dict`, ensuring immediate execution.

## Core Endpoint

`POST /api/coupons/validate`

### Request Body

```json
{
  "code": "CUPON10",
  "totalAmount": 100.0
}
```

### Expected Responses

**Valid Coupon**

```json
{
  "valid": true,
  "discount": 10.0,
  "finalAmount": 90.0,
  "message": "¡Cupón aplicado con éxito!"
}
```

**Invalid or Inactive Coupon**

```json
{
  "valid": false,
  "discount": 0.0,
  "finalAmount": 100.0,
  "message": "Cupón inválido"
}
```

## Sample In-Memory Data

| Code     | Type       | Value  | Active |
| -------- | ---------- | ------ | ------ |
| CUPON10  | Percentage | 10%    | Yes    |
| KICKS20  | Percentage | 20%    | Yes    |
| FIJO15   | Fixed Amount | $15.00 | Yes  |
| EXPIRED  | Percentage | 50%    | No     |

## Tech Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Validation / Typing:** Pydantic v2
- **ASGI Server:** Uvicorn

## Requirements & Setup

### Environment

- Python 3.11 or newer installed
- `pip` available on your PATH

### Run the API Locally

Navigate to the project root directory and execute:

```bash
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

**Linux / macOS:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

The server will initialize and listen for requests at: [http://localhost:8080](http://localhost:8080)

Interactive docs are available at:
- Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)
- ReDoc: [http://localhost:8080/redoc](http://localhost:8080/redoc)

## Automated Testing via cURL

### 1. Test 10% Off (`CUPON10`)

**Windows (Command Prompt):**

```bat
curl -X POST http://localhost:8080/api/coupons/validate ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"CUPON10\",\"totalAmount\":100.0}"
```

Expected result: `discount: 10.0`, `finalAmount: 90.0`

### 2. Test 20% Off (`KICKS20`)

**Windows (Command Prompt):**

```bat
curl -X POST http://localhost:8080/api/coupons/validate ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"KICKS20\",\"totalAmount\":100.0}"
```

Expected result: `discount: 20.0`, `finalAmount: 80.0`

### 3. Test Fixed $15 Off (`FIJO15`)

**Windows (Command Prompt):**

```bat
curl -X POST http://localhost:8080/api/coupons/validate ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"FIJO15\",\"totalAmount\":100.0}"
```

Expected result: `discount: 15.0`, `finalAmount: 85.0`

### 4. Test Invalid Code

**Windows (Command Prompt):**

```bat
curl -X POST http://localhost:8080/api/coupons/validate ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"NOEXISTE\",\"totalAmount\":100.0}"
```

Expected result: `valid: false`, `discount: 0.0`, `finalAmount: 100.0`

### 5. Test Inactive Coupon (`EXPIRED`)

**Windows (Command Prompt):**

```bat
curl -X POST http://localhost:8080/api/coupons/validate ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"EXPIRED\",\"totalAmount\":100.0}"
```

Expected result: returns the standard invalid schema (same as a missing code).

### Unix Syntax (Linux / macOS / WSL)

```bash
curl -X POST http://localhost:8080/api/coupons/validate \
  -H "Content-Type: application/json" \
  -d '{"code":"CUPON10","totalAmount":100.0}'
```


