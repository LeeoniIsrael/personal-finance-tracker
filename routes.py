import requests
from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from models import Transaction
from config import Config

@app.route('/', methods=['GET'])
def index():
    return render_template("main.html")
    


@app.route('/user_add', methods=['POST', 'GET'])
def user_add():
    slay = ""
    if request.method == 'GET':
        return render_template("add.html")
    data = request.json
    print(data)
    transaction = Transaction(
        amount=data['amount'],
        currency=data['currency'],
        type=data['type'],
        description=data.get('description')
    )
    print(transaction)
    db.session.add(transaction)
    db.session.commit()
    return render_template("add.html")
    #return render_template("index.html",slay="Transaction Added!")

@app.route('/user_view', methods=['POST', 'GET'])
def user_view():
    history = Transaction.query.all()
    return render_template("view.html", history=history)
    #return render_template("index.html",slay="Transaction Added!")

@app.route('/user_convert', methods=['POST', 'GET'])
def user_convert():
    if request.method == "GET":
        return render_template("convert.html")
    data = request.json
    print(data)
    amount = data['amount']
    from_currency = data['from']
    to_currency = data['to']
    api_key = Config.EXCHANGE_RATE_API_KEY  # Replace with your actual API key
    url = f'https://api.exchangeratesapi.io/v1/convert?access_key={api_key}&from={from_currency}&to={to_currency}&amount={amount}'   
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data['success']:
            converted_amount = data['result']
            print(converted_amount)
            return render_template('convert.html', converted_amount=converted_amount, currency=to_currency)
        else:
            return render_template('convert.html', error="Failed to convert currency. Check your parameters.")
    except requests.exceptions.RequestException as e:
        return render_template("convert.html", error="Request failed")
    #return render_template("index.html",slay="Transaction Added!")


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    transaction = Transaction(
        amount=data['amount'],
        currency=data['currency'],
        type=data['type'],
        description=data.get('description', '')
    )
    print(transaction)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully'}), 201

@app.route('/transactions', methods=['GET', 'POST'])
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

@app.route('/convert_currency', methods=['GET', 'POST'])
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
