import unittest
from unittest.mock import patch
from app import app, db
from models import Transaction

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        # Push application context
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
        # Pop application context
        self.app_context.pop()

    def test_add_transaction(self):
        response = self.app.post('/add_transaction', json={
            'amount': 100.0,
            'currency': 'USD',
            'type': 'income',
            'description': 'Salary'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Transaction added successfully', response.data)

    def test_get_transactions(self):
        self.app.post('/add_transaction', json={
            'amount': 100.0,
            'currency': 'USD',
            'type': 'income',
            'description': 'Salary'
        })
        response = self.app.get('/transactions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Salary', response.data)

    @patch('routes.requests.get')
    def test_convert_currency(self, mock_get):
        mock_response = {
            'success': False,
            'error': 'Failed to convert currency. Check your parameters.'
        }
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response

        response = self.app.get('/convert_currency?amount=100&from=USD&to=EUR')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Failed to convert currency', response.data)

if __name__ == '__main__':
    unittest.main()
