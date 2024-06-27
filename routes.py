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
    amount = request.args.get('amount', type=float)
    from_currency = request.args.get('from', type=str)
    to_currency = request.args.get('to', type=str)

    api_key = Config.EXCHANGE_RATE_API_KEY  # Replace with your actual API key
    url = f'https://api.exchangeratesapi.io/v1/convert?access_key={api_key}&from={from_currency}&to={to_currency}&amount={amount}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data['success']:
            converted_amount = data['result']
            return jsonify({
                'success': True,
                'from': from_currency,
                'to': to_currency,
                'amount': amount,
                'converted_amount': converted_amount
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to convert currency. Check your parameters.'
            }), 400

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Request failed: {str(e)}'
        }), 500