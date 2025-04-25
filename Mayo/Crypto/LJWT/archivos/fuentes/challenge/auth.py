from Crypto.Util.number import bytes_to_long
from hashlib import sha256
import base64
import json

def encode(data):
    """Encode string using URL-safe base64.
    Args:
        data: String to encode
    Returns:
        str: Base64 encoded string
    """
    return base64.urlsafe_b64encode(data.encode()).decode()

def decode(data):
    """Decode URL-safe base64 string.
    Args:
        data: Base64 string to decode
    Returns:
        str: Decoded string
    """
    return base64.urlsafe_b64decode(data.encode()).decode()

def sign(message, key):
    """Sign message using LJWT (Linear JWT) algorithm.
    Args:
        message: Message to sign
        key: Tuple (a, b, p) where:
            a: Linear coefficient
            b: Constant term
            p: Modulus
    Returns:
        int: Signature value
    """
    a, b, p = key
    h = sha256(message.encode()).digest()
    h = bytes_to_long(h)
    return (a * h + b) % p

def verify(message, signature, key):
    """Verify LJWT signature.
    Args:
        message: Original message
        signature: Signature to verify
        key: Tuple (a, b, p) for verification
    Returns:
        bool: True if signature is valid
    """
    a, b, p = key
    h = sha256(message.encode()).digest()
    h = bytes_to_long(h)
    return signature == (a * h + b) % p

def generate_token(user_data, key):
    """Generate LJWT token for user.
    Args:
        user_data: Dictionary with user information
        key: Tuple (a, b, p) for signing
    Returns:
        str: LJWT token in format header.payload.signature
    """
    header = json.dumps({"alg": "AHS256"})
    payload = json.dumps(user_data)
    data = f"{header}.{payload}"
    signature = sign(data, key)
    return f"{encode(header)}.{encode(payload)}.{encode(str(signature))}"

def validate_token(token, key):
    """Validate LJWT token and extract payload.
    Args:
        token: LJWT token string
        key: Tuple (a, b, p) for verification
    Returns:
        dict: Token payload if valid, None otherwise
    """
    if not token or token.count('.') != 2:
        return None

    try:
        encoded_header, encoded_payload, encoded_signature = token.split('.')
        header = json.loads(decode(encoded_header))
        payload = json.loads(decode(encoded_payload))
        data = f'{json.dumps(header)}.{json.dumps(payload)}'

        if header.get("alg") != "AHS256":
            return None

        signature = int(decode(encoded_signature))
        if not verify(data, signature, key):
            return None

        return payload
    except Exception as e:
        print(f"Token validation error: {e}")
        return None
