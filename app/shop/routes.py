from flask import Blueprint, jsonify, request, session
from app import mongo
from passlib.hash import sha256_crypt
from marshmallow import Schema, fields, ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


menu_bp = Blueprint('menu', __name__)
@menu_bp.route('/create_menu', methods=['POST'])
def create_menu():
    if request.method == 'POST':
        menu_data = [
            {
                'name': 'Pizza',
                'price': 50,
                'topping': ['Papper', 'Blueberry', 'Apple slices'],
                'filling': ['Tuna', 'Cheese', 'Chicken']
            },
            {
                'name': 'Doughnut',
                'price': 20,
                'topping': ['Blueberry', 'Cheese', 'Sugar Glaze'],
                'filling': ['Apple slices', 'Milk cream', 'Blueberry']
            },
            {
                'name': 'Pie',
                'price': 45,
                'topping': ['Cheese', 'Chicken', 'Papper'],
                'filling': ['Chese', 'Tomato', 'Tuna']
            }
        ]

        # Insert each menu item into the database as separate documents
        for item in menu_data:
            mongo.db.menu.insert_one(item)

        return jsonify({'message': 'Menu created successfully'})

    return jsonify({'error': 'Unsupported HTTP method!'})

 
@menu_bp.route('/create_toppings', methods=['POST'])
def create_toppings():
    toppings_data = {
        'Pie': [
            {'name': 'Cheese', 'price': 12},
            {'name': 'Chicken', 'price': 18},
            {'name': 'Papper', 'price': 8}
        ],
        'Doughnut': [
            {'name': 'Blueberry', 'price': 12},
            {'name': 'Cheese', 'price': 12},
            {'name': 'Sugar Glaze', 'price': 10}
        ],
        'Pizza': [
            {'name': 'Papper', 'price': 8},
            {'name': 'Blueberry', 'price': 12},
            {'name': 'Apple slices', 'price': 14}
        ]
    }

    # Insert toppings into the database
    for item, toppings in toppings_data.items():
        for topping in toppings:
            topping['item'] = item
            mongo.db.toppings.insert_one(topping)  # Menggunakan insert_one untuk satu dokumen

    return jsonify({'message': 'Toppings created successfully'})

@menu_bp.route('/create_fillings', methods=['POST'])
def create_fillings():
    fillings_data = {
        'Pie': [
            {'name': 'Chese', 'price': 12},
            {'name': 'Tomato', 'price': 9},
            {'name': 'Tuna', 'price': 20}
        ],
        'Doughnut': [
            {'name': 'Apple slices', 'price': 14},
            {'name': 'Milk cream', 'price': 10},
            {'name': 'Blueberry', 'price': 12}
        ],
        'Pizza': [
            {'name': 'Tuna', 'price': 20},
            {'name': 'Cheese', 'price': 12},
            {'name': 'Chicken', 'price': 18}
        ]
    }

    # Insert fillings into the database
    for item, fillings in fillings_data.items():
        for filling in fillings:
            filling['item'] = item
            mongo.db.fillings.insert_one(filling)

    return jsonify({'message': 'Fillings created successfully'})

@menu_bp.route('/menu_prices', methods=['GET'])
def get_menu_prices():
    menu_prices = get_all_menu_prices()
    topping_prices = get_all_topping_prices()
    filling_prices = get_all_filling_prices()

    return jsonify({
        'menu_prices': menu_prices,
        'topping_prices': topping_prices,
        'filling_prices': filling_prices
    })

def get_all_menu_prices():
    # Query semua menu dan harga dari koleksi menu di MongoDB
    all_menu = mongo.db.menu.find({}, {'items.name': 1, 'items.price': 1, '_id': 0})

    menu_prices = {}
    for menu in all_menu:
        for item in menu['items']:
            menu_prices[item['name']] = item['price']

    return menu_prices

def get_all_topping_prices():
    # Query semua topping dan harga dari koleksi toppings di MongoDB
    all_toppings = mongo.db.toppings.find({}, {'name': 1, 'price': 1, '_id': 0})

    topping_prices = {}
    for topping in all_toppings:
        topping_prices[topping['name']] = topping['price']

    return topping_prices

def get_all_filling_prices():
    # Query semua filling dan harga dari koleksi fillings di MongoDB
    all_fillings = mongo.db.fillings.find({}, {'name': 1, 'price': 1, '_id': 0})

    filling_prices = {}
    for filling in all_fillings:
        filling_prices[filling['name']] = filling['price']

    return filling_prices
