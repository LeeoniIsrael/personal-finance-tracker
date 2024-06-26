import requests
from flask import current_app

def convert_currency(amount, from_currency, to_currency):
    api_key = current_app.config['d6058b00ce51054f8ace1c2c']
    base_url = 'http://api.exchangeratesapi.io/v1/latest'
    params = {
        'access_key': api_key,
        'symbols': f'{from_currency},{to_currency}'
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if 'error' in data:
        return None, data['error']

    from_rate = data['rates'].get(from_currency)
    to_rate = data['rates'].get(to_currency)
    
    if not from_rate or not to_rate:
        return None, f"One of the specified currencies is not supported: {from_currency} or {to_currency}"

    converted_amount = (amount / from_rate) * to_rate
    return converted_amount, None
