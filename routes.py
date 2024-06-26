from flask import request, jsonify, abort
from app import app, db
from models import User, Transaction
import requests

API_KEY = 'your_exchange_rate_api_key'
API_URL = 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(API_KEY)

@app.route('/convert', methods=['GET'])
def convert_currency():
    amount = float(request.args.get('amount'))
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    response = requests.get(API_URL)
    data = response.json()

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch exchange rates'}), 500

    if from_currency not in data['conversion_rates'] or to_currency not in data['conversion_rates']:
        return jsonify({'error': 'Invalid currency code'}), 400

    rate = data['conversion_rates'][to_currency] / data['conversion_rates'][from_currency]
    converted_amount = amount * rate

    return jsonify({'amount': converted_amount}), 200


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.id), 201

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    new_transaction = Transaction(amount=data['amount'], category=data['category'], user_id=data['user_id'])
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(new_transaction.id), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([trans.to_dict() for trans in transactions])

@app.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    data = request.get_json()
    transaction = Transaction.query.get_or_404(id)
    transaction.amount = data['amount']
    transaction.category = data['category']
    db.session.commit()
    return jsonify(transaction.to_dict())

@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return '', 204

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'username': user.username, 'email': user.email})

@app.route('/users/<int:id>/transactions', methods=['GET'])
def get_user_transactions(id):
    user = User.query.get_or_404(id)
    transactions = Transaction.query.filter_by(user_id=id).all()
    return jsonify([trans.to_dict() for trans in transactions])

