Shortlink service (Flask)

What it does

- POST `/links` — create a short code for a URL. Body: JSON {"url": "https://..."}
  - Validates shape and content strictly; returns `400` with `{"error":"validation_failed","fields":{...}}` naming each failing field.
  - Idempotent: posting the same URL twice returns the same code (201 on create, 200 if already existed).
- GET `/<code>` — redirects to the stored URL and increments a click counter.
  - Returns `404` with a `fields` message for unknown codes.
- GET `/links/<code>/stats` — returns JSON with `clicks` and `url`.

Redirect choice

This service uses `302` (Found) redirects to avoid browsers permanently caching shortlink mappings. To change to `301` (permanent), edit the redirect code in [shortlink/views.py](shortlink/views.py#L1-L200) and update clients accordingly.

Conformance to the brief

- **Malformed input → 400**: Validation lives at the edge and returns a `fields` map naming problems. See [shortlink/validators.py](shortlink/validators.py#L1-L200).
- **Never 500 for bad input**: HTTP errors from validation are preserved; unexpected server errors are logged and return a generic `500` only for genuine server faults. See [shortlink/views.py](shortlink/views.py#L1-L200).
- **Idempotent creates**: Submitting the same URL returns the same code; uniqueness enforced by DB and lookup. See [shortlink/db.py](shortlink/db.py#L1-L200) and [shortlink/views.py](shortlink/views.py#L1-L200).
- **Unknown code → 404**: Follow returns `404` for unknown codes and does not return 200. See [shortlink/views.py](shortlink/views.py#L1-L200).

Tests

Run the tests with:

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

Database

A local SQLite DB is created automatically; when running tests a temporary DB is used by the test suite.

Notes

- If you want stricter limits (payload size, rate limits) or to change redirect semantics, I can add that.

This project meets the assignment requirements: validation at the boundary, named field errors, idempotent creation, proper 404s, and a documented redirect choice.

## M. Hassan Idrees