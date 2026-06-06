# TarkaX API Documentation

The TarkaX API Platform provides secure, programmatic access to the underlying AI Intelligence and Risk Projection engines used by the TarkaX platform.

## Authentication

All endpoints under the `/api/v1` namespace require an API key to authenticate requests. The API key must be sent via the `X-API-Key` header.

```http
X-API-Key: tk_live_xxxxxxxxx
```

If the key is invalid or revoked, the API will return a `401 Unauthorized` or `403 Forbidden` response. Rate limits apply based on the tier of your API key. Exceeding the rate limit will return a `429 Too Many Requests`.

---

## AI Audit API

Submit an assessment payload and receive intelligence through the exact same engine used by the TarkaX website.

### Request

**Endpoint:** `POST /api/v1/audit`

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: <your_api_key>`

**Body Example:**

```json
{
  "form_response": {
    "question_1": "answer",
    "question_2": 3
  },
  "evidence_response": {},
  "industry_type": "Technology"
}
```

### Responses

**Success (200 OK)**

Returns the full `AuditResponse` intelligence payload, which persists the audit into your organization's history.

```json
{
  "id": "e0e2d142-b8ec-4581-ba59-1e5b85e05bb6",
  "org_id": "71b2d142-c8ec-4581-ba59-1e5b85e05ab1",
  "user_id": "8a02d142-a8ec-4581-ba59-1e5b85e05fc4",
  "total_score": 67,
  "rating": "Developing",
  "intelligence": {
    "executive_summary": { ... },
    "findings": [ ... ],
    "recommendations": [ ... ],
    "failure_intelligence": [ ... ]
  },
  "status": "complete",
  "industry_type": "Technology",
  "created_at": "2024-03-01T12:00:00Z"
}
```

**Errors**

- `400 Bad Request`: Validation error in payload or missing active user in the organization.
- `401 Unauthorized`: Missing or invalid API Key.
- `403 Forbidden`: Revoked API Key.
- `429 Too Many Requests`: Rate limit exceeded.

---

## Risk Projection API

A stateless calculation API that generates a future-state risk projection based on scoring inputs. No database records are created or persisted.

### Request

**Endpoint:** `POST /api/v1/risk`

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: <your_api_key>`

**Body Example:**

```json
{
  "scores": {
    "dimensions": {
      "awareness": 60,
      "adoption": 72,
      "integration": 40,
      "governance": 35,
      "roi": 58
    },
    "missing_data_flags": [],
    "contradictions": [],
    "evidence_quality_score": 80
  },
  "findings": []
}
```

### Responses

**Success (200 OK)**

```json
{
  "risk_level": "High",
  "risk_score": 67,
  "risk_trend": "Stable",
  "confidence": 100,
  "explanation": "Risk is high because governance maturity gap.",
  "risk_drivers": [
    "Governance maturity gap",
    "Integration maturity gap",
    "ROI measurement gap"
  ],
  "risk_timeline": {
    "near_term": [
      "Operational inefficiencies expand due to uncoordinated usage."
    ],
    "mid_term": [
      "Governance and adoption gaps begin affecting execution quality."
    ],
    "long_term": [
      "Strategic value realization becomes increasingly difficult."
    ]
  }
}
```

**Errors**

- `401 Unauthorized`: Missing or invalid API Key.
- `403 Forbidden`: Revoked API Key.
- `429 Too Many Requests`: Rate limit exceeded.
- `422 Unprocessable Entity`: The request body structure is invalid.
