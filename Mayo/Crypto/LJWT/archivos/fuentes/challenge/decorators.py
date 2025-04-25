from functools import wraps
from flask import request, redirect, url_for
from auth import validate_token
from utils import load_secret_key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        SECRET_KEY = load_secret_key()
        user_data = validate_token(token, SECRET_KEY) if token else None

        if not user_data:
            return redirect(url_for('index'))

        request.current_user = user_data
        return f(*args, **kwargs)
    return decorated