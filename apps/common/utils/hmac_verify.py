import hmac
import hashlib


def verify_hmac_signature(payload: bytes, signature: str, secret: str) -> bool:
  
    computed_hmac = hmac.new(
        key=secret.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed_hmac, signature)