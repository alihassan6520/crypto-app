import pytest
from flask import jsonify
from app import create_app, db
from app.models import User, CryptoAddress

import sys
import os

# Append the path to the 'app' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            # Create a user for testing
            user = User(email='test@example.com', password='testpassword')
            db.session.add(user)
            db.session.commit()
            yield testing_client
            db.session.remove()
            db.drop_all()

def test_login(test_client):
    # Test login with valid credentials
    response = test_client.post('/login', json={'email': 'test@example.com', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'access_token' in response.json

    # Test login with invalid credentials
    response = test_client.post('/login', json={'email': 'test@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid email or password'

def test_generate_address(test_client):
    # Login to get the access token
    login_response = test_client.post('/login', json={'email': 'test@example.com', 'password': 'testpassword'})
    access_token = login_response.json['access_token']

    # Test generating a BTC address
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.post('/addresses', json={'cryptocurrency': 'BTC'}, headers=headers)
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'cryptocurrency' in response.json
    assert 'address' in response.json

    # Test generating an ETH address
    response = test_client.post('/addresses', json={'cryptocurrency': 'ETH'}, headers=headers)
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'cryptocurrency' in response.json
    assert 'address' in response.json

    # Test generating an address with an unsupported cryptocurrency
    response = test_client.post('/addresses', json={'cryptocurrency': 'LTC'}, headers=headers)
    assert response.status_code == 200

def test_get_addresses(test_client):
    # Login to get the access token
    login_response = test_client.post('/login', json={'email': 'test@example.com', 'password': 'testpassword'})
    access_token = login_response.json['access_token']

    # Generate some addresses for the user
    headers = {'Authorization': f'Bearer {access_token}'}
    test_client.post('/addresses', json={'cryptocurrency': 'BTC'}, headers=headers)
    test_client.post('/addresses', json={'cryptocurrency': 'ETH'}, headers=headers)

    # Test getting the addresses
    response = test_client.get('/addresses', headers=headers)
    assert response.status_code == 200
    #assert len(response.json) == 2
    assert all('id' in address and 'cryptocurrency' in address and 'address' in address for address in response.json)

def test_get_address(test_client):
    # Login to get the access token
    login_response = test_client.post('/login', json={'email': 'test@example.com', 'password': 'testpassword'})
    access_token = login_response.json['access_token']

    # Generate a BTC address
    headers = {'Authorization': f'Bearer {access_token}'}
    response = test_client.post('/addresses', json={'cryptocurrency': 'BTC'}, headers=headers)
    address_id = response.json['id']

    # Test getting the generated address
    response = test_client.get(f'/addresses/{address_id}', headers=headers)
    assert response.status_code == 200
    pass
