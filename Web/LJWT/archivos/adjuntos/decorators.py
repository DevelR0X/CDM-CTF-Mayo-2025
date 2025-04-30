from flask import request, redirect, url_for, jsonify

from auth import validate_token
from utils import load_secret_key
from database import DATABASE

from functools import wraps
import sqlite3

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


def handle_exceptions(func):
    """Decorator to handle generic exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error:
            return jsonify({'status': 'error', 'message': 'Error en la base de datos'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': 'Error en el servidor'}), 500
    return wrapper

def with_db_connection(func):
    """Decorator to provide a database connection."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with sqlite3.connect(DATABASE) as conn:
            return func(conn, *args, **kwargs)
    return wrapper