# app/routes.py

from flask import Blueprint, jsonify, request
from app.models import User, CryptoAddress
#from app.utils import generate_cryptocurrency_address
from crypto.address import generate_cryptocurrency_address
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db
from app.utils import add_user

api_bp = Blueprint('api', __name__)
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify(message='Invalid email or password'), 401



@api_bp.route('/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    addresses = CryptoAddress.query.filter_by(user_id=user_id).all()
    address_list = [
            {
                'id': address.id,
                'cryptocurrency': address.cryptocurrency,
                'address': address.address
            }
            for address in addresses
        ]
    return jsonify(address_list), 200

@api_bp.route('/addresses', methods=['POST'])
@jwt_required()
def generate_address():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.get_json()
    cryptocurrency = data.get('cryptocurrency')

    address = generate_cryptocurrency_address(cryptocurrency)

    crypto_address = CryptoAddress(user=user, cryptocurrency=cryptocurrency, address=address)
    db.session.add(crypto_address)
    db.session.commit()

    response = {
        'id': crypto_address.id,
        'cryptocurrency': crypto_address.cryptocurrency,
        'address': crypto_address.address
    }
    return jsonify(response), 200

@api_bp.route('/addresses/<int:address_id>', methods=['GET'])
@jwt_required()
def get_address(address_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    address = CryptoAddress.query.filter_by(id=address_id, user=user).first()
    if address:
        return jsonify(address=address.address), 200

    return jsonify(message='Address not found'), 404

@api_bp.route('/add_user')
def add_user_route():
    email = 'user@example.com'
    password = 'password123'
    add_user(email, password)
    return 'User added successfully'
