from Crypto.Util.number import bytes_to_long
from hashlib import sha256
import requests
import base64
import json

p = 58507437344581102585324080193177868533195535532587539416354635038925019187417

BASE_URL = "http://127.0.0.1:5000"

users = [
    {"username": "D-Cryp7_0", "email": "dcryp7@hed.cl", "password": "test"},
    {"username": "D-Cryp7_1", "email": "dcryp7@hed.cl", "password": "test"}
]

def register(params):
    response = requests.post(f"{BASE_URL}/register", json = params).content
    return response

def login(params):
    response = requests.post(f"{BASE_URL}/login", json = params)
    if json.loads(response.content)["status"] == "success":    
        return response.cookies["token"]
    return response.content

def encode(data):
    return base64.urlsafe_b64encode(data.encode()).decode()

def decode(data):
    return base64.urlsafe_b64decode(data.encode()).decode()

def process_token(token):
    encoded_header, encoded_payload, encoded_signature = token.split(".")
    
    header = decode(encoded_header)
    payload = decode(encoded_payload)
    signature = decode(encoded_signature)

    h = f"{header}.{payload}"
    print(h)
    h = sha256(h.encode()).digest()
    h = bytes_to_long(h)

    s = int(signature)

    return h, s
    
tokens = []
hashes = []
signatures = []

for user in users:
    response = register(user)
    print(response)

    token = login(user)
    tokens.append(token)

    h, s = process_token(token)
    hashes.append(h)
    signatures.append(s)


h1, h2 = hashes
s1, s2 = signatures

a = (s1 - s2) * pow(h1 - h2, -1, p) % p
b = (s1 - a*h1) % p

# Target data
header = {"alg": "AHS256"}
payload = {"id": 1, "username": "Administrador", "access_level": 3, "email": "admin@hed.cl"}

header = json.dumps(header)
payload = json.dumps(payload)

data = f"{header}.{payload}"

h = bytes_to_long(sha256(data.encode()).digest())
print(h)

signature = (a * h + b) % p
print(signature)

encoded_header = encode(header)
encoded_payload = encode(payload)
encoded_signature = encode(str(signature))

token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"

print(token)