import hashlib

def make_code(url: str) -> str:
    digest = hashlib.sha256(url.encode()).hexdigest()
    return digest[:8]
