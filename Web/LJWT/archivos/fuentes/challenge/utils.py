import re
import os

def validate_input(input_str, max_length = 100):
    """Validate user input string."""
    if not isinstance(input_str, str):
        return False
    if not input_str or len(input_str) > max_length:
        return False
    return re.match(r'^[\w.@-]+$', input_str) is not None

def check_fields(data, required_fields):
    """Check if required fields are present and valid."""
    if not data or not all(k in data for k in required_fields):
        return False, 'Datos incompletos'
    if not all(validate_input(data[k]) for k in required_fields):
        return False, 'Caracteres no permitidos'
    return True, None

def load_secret_key():
    """Load secret key from environment variable."""
    secret = os.getenv("SECRET_KEY")
    if not secret:
        return None
    try:
        return tuple(int(param) for param in secret.split(","))
    except (ValueError, TypeError):
        print("Error: Invalid SECRET_KEY format")
        return None
