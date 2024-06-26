from flask import request, jsonify, abort
from app import app, db
from models import User, Transaction
from currency_converter import convert_currency

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

@app.route('/convert', methods=['GET'])
def convert():
    amount = request.args.get('amount', type=float)
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    if not amount or not from_currency or not to_currency:
        return jsonify({'error': 'Missing required parameters'}), 400

    result, error = convert_currency(amount, from_currency, to_currency)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'amount': amount, 'from': from_currency, 'to': to_currency, 'result': result})
