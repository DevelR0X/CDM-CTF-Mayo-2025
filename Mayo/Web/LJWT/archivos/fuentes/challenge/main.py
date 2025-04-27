from flask import Flask

from routes import register_routes
from database import init_db

from secrets import randbelow
import json
import os

def create_app():
    app = Flask(__name__)
    register_routes(app)
    return app

def generate_secret():
    with open("./.well-known/jwks.json", "r") as public_key:
        p = int(json.load(public_key)["p"])
    a, b = [ randbelow(p) for _ in range(2) ]
    os.environ["SECRET_KEY"] = f"{a},{b},{p}"

if __name__ == '__main__':
    init_db()
    generate_secret()
    
    app = create_app()
    app.run(host = "0.0.0.0", port = 5000, debug = False)