from flask import Blueprint, jsonify, request, session
from app import mongo
from passlib.hash import sha256_crypt
from marshmallow import Schema, fields, ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


order_bp = Blueprint('order', __name__)

@order_bp.route('/place_order', methods=['POST'])
def place_order():
    if request.method == 'POST':
        data = request.get_json()

        # Ambil data menu, topping, dan filling dari request
        selected_menu = data.get('menu')
        selected_toppings = data.get('topping')
        selected_fillings = data.get('filling')

        # Ambil harga dari menu yang dipilih
        menu_price = get_menu_price(selected_menu)

        # Hitung harga dari topping yang dipilih
        topping_price = calculate_toppings_price(selected_toppings)

        # Hitung harga dari filling yang dipilih
        filling_price = calculate_fillings_price(selected_fillings)

        # Hitung total harga
        total_price = menu_price + topping_price + filling_price

        return jsonify({'total_price': total_price})

    return jsonify({'error': 'Unsupported HTTP method!'})
def get_menu_price(menu_name):
    # Query koleksi menu di MongoDB berdasarkan nama menu
    menu = mongo.db.menu.find_one({'name': menu_name})

    if menu:
        print(menu['price'])
        return menu['price']
    
    return 0

def calculate_toppings_price(selected_toppings):
    total_topping_price = 0

    # Mengambil harga topping dari MongoDB
    for topping in selected_toppings:
        topping_price = mongo.db.toppings.find_one({'name': topping})
        if topping_price:
            total_topping_price += topping_price['price']
    print(total_topping_price)
    return total_topping_price

def calculate_fillings_price(selected_fillings):
    total_filling_price = 0

    # Mengambil harga filling dari MongoDB
    for filling in selected_fillings:
        filling_price = mongo.db.fillings.find_one({'name': filling})
        if filling_price:
            total_filling_price += filling_price['price']
    print(total_filling_price)
    return total_filling_price