from flask import Flask, jsonify, request
import jwt
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

# Load private and public keys
with open('private_key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

with open('public_key.pem', 'rb') as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

@app.route('/auth', methods=['POST'])
def auth():
    username = request.json.get('username')
    if username:
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, private_key, algorithm='RS256')
        return jsonify({'token': token.decode('utf-8')})  # Decode bytes to string
    return jsonify({'message': 'Missing username'}), 400

@app.route('/jwks', methods=['GET'])
def jwks():
    public_numbers = public_key.public_numbers()
    return jsonify({
        'keys': [{
            'kty': 'RSA',
            'n': public_numbers.n,
            'e': public_numbers.e,
            'kid': 'unique-key-id'
        }]
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
