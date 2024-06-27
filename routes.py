import requests
from flask import request, jsonify
from app import app, db
from models import Transaction
from config import Config

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    transaction = Transaction(
        amount=data['amount'],
        currency=data['currency'],
        type=data['type'],
        description=data.get('description', '')
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully'}), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    result = []
    for trans in transactions:
        result.append({
            'amount': trans.amount,
            'currency': trans.currency,
            'type': trans.type,
            'description': trans.description
        })
    return jsonify(result)

@app.route('/convert_currency', methods=['GET'])
def convert_currency():
    amount = float(request.args.get('amount', 0))
    from_currency = request.args.get('from', 'USD')
    to_currency = request.args.get('to', 'EUR')

    url = f'https://api.exchangeratesapi.io/latest?base={from_currency}&symbols={to_currency}'
    response = requests.get(url)
    data = response.json()

    if 'rates' not in data or to_currency not in data['rates']:
        return jsonify({"error": "Conversion rate not available"}), 400

    rate = data['rates'][to_currency]
    converted_amount = amount * rate

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted_amount": converted_amount
    }), 200

