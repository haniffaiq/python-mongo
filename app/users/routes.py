from flask import Blueprint, jsonify, request
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from app.models import User  # Mengimpor model User
from marshmallow import Schema, fields, ValidationError
from app import mongo

users_bp = Blueprint('users', __name__)
class UserSchema(Schema):
    name = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

# Fungsi untuk memeriksa ketersediaan username
def validate_username(username):
    users_collection = mongo.db.users
    existing_user = users_collection.find_one({'username': username})
    if existing_user:
        raise ValidationError('Username already exists')

UserSchema.validate_username = validate_username  # Menambahkan validasi custom ke schema

mongo.db.users.create_index([('username', 1)], unique=True)

@users_bp.route('/api/create', methods=['POST'])
def create_user():
    data = request.get_json()

    # Melakukan validasi menggunakan Marshmallow
    try:
        validated_data = UserSchema().load(data)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    users_collection = mongo.db.users

    try:
        # Menyimpan objek User ke dalam database
        user = User(**validated_data)
        user_id = users_collection.insert_one(user.__dict__).inserted_id
        return jsonify({'message': 'User created', 'id': str(user_id)}), 201
    except DuplicateKeyError:
        return jsonify({'error': 'Username already exists'}), 409
 
@users_bp.route('/api/read/<string:user_id>', methods=['GET'])
def read_user(user_id):
    try:
        # Attempt to convert the string to an ObjectId
        object_id = ObjectId(user_id)
        users_collection = mongo.db.users

        # Mencari pengguna dalam database menggunakan model User
        user_data = users_collection.find_one({'_id': object_id})
        if user_data:
            user = User(**user_data)  # Membuat objek User dari data pengguna
            user._id = str(user._id)  # Mengubah _id menjadi string
            return jsonify(user.__dict__)  # Mengembalikan data pengguna sebagai JSON
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid user ID'}), 400

@users_bp.route('/api/update/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    users_collection = mongo.db.users
    try:
        object_id = ObjectId(user_id)

        # Validasi data yang diterima menggunakan Marshmallow
        try:
            validated_data = UserSchema().load(data)
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400

        # Menggunakan model User untuk memperbarui data pengguna
        result = users_collection.update_one({'_id': object_id}, {'$set': validated_data})
        if result.modified_count > 0:
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid user ID'}), 400

@users_bp.route('/api/delete/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users_collection = mongo.db.users
    try:
        object_id = ObjectId(user_id)

        # Validasi apakah pengguna ada sebelum menghapus
        if not users_collection.find_one({'_id': object_id}):
            return jsonify({'message': 'User not found'}), 404

        # Menggunakan model User untuk menghapus pengguna
        result = users_collection.delete_one({'_id': object_id})
        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'error': 'Invalid user ID'}), 400
