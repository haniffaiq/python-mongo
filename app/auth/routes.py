from flask import Blueprint, jsonify, request, session
from app import mongo
from passlib.hash import sha256_crypt
from marshmallow import Schema, fields, ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


auth_bp = Blueprint('auth', __name__)

class AuthSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

def validate_username(username):
    users_collection = mongo.db.users
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        raise ValidationError('Username already exists')

AuthSchema.validate_username = validate_username
mongo.db.users.create_index([('username', 1)], unique=True)

@auth_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        validated_data = AuthSchema().load(data)
        users_collection = mongo.db.users
        existing_user = users_collection.find_one({'username': data['username']})

        if existing_user is None:
            password = sha256_crypt.encrypt(validated_data['password'])
            users_collection.insert_one({'username': validated_data['username'], 'password': password})
            return jsonify({'message': 'Registration successful!'})
        return jsonify({'error': 'Username already exists!'})

    return jsonify({'error': 'Unsupported HTTP method!'})

@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        validated_data = AuthSchema().load(data)
        users_collection = mongo.db.users
        user = users_collection.find_one({'username': validated_data['username']})

        if user:
            if sha256_crypt.verify(validated_data['password'], user['password']):

                access_token = create_access_token(identity=user['username'])
                return jsonify({'access_token': access_token})
        
        return jsonify({'error': 'Invalid username or password'})

    return jsonify({'error': 'Unsupported HTTP method!'})