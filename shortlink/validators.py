from urllib.parse import urlparse

def validate_create_link(data):
    errors = {}

    if not isinstance(data, dict):
        return {"_body": "must be a JSON object"}
    allowed_fields = {"url"}
    unknown = set(data.keys()) - allowed_fields
    if unknown:
        errors["_unknown"] = f"unexpected fields: {', '.join(sorted(unknown))}"
        
    if "url" not in data:
        errors["url"] = "is required"
    elif not isinstance(data["url"], str):
        errors["url"] = "must be a string"
    elif len(data["url"]) == 0:
        errors["url"] = "must not be empty"
    elif len(data["url"]) > 2048:
        errors["url"] = "must be at most 2048 characters"
    else:
        parsed = urlparse(data["url"])
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            errors["url"] = "must be a valid http(s) URL"
    return errors
