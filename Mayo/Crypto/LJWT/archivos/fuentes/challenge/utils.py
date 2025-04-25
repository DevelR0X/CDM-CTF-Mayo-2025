import re
import os

def validate_input(input_str, max_length = 100):
    """Validate user input string.
    Args:
        input_str: String to validate
        max_length: Maximum allowed length (default: 100)
    Returns:
        bool: True if input is valid, False otherwise
    """
    if not isinstance(input_str, str):
        return False
    if not input_str or len(input_str) > max_length:
        return False
    return re.match(r'^[\w.@-]+$', input_str) is not None

def load_secret_key():
    """Load secret key from environment variable.
    Returns:
        tuple: (a, b, p) for LJWT signing or None if not found
    """
    secret = os.getenv("SECRET_KEY")
    if not secret:
        return None
    try:
        return tuple(int(param) for param in secret.split(","))
    except (ValueError, TypeError):
        print("Error: Invalid SECRET_KEY format")
        return None
