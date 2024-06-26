import unittest
from app import app, db
from models import User, Transaction

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        response = self.app.post('/users', json={'username': 'testuser', 'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 201)

    def test_add_transaction(self):
        self.app.post('/users', json={'username': 'testuser', 'email': 'testuser@example.com'})
        response = self.app.post('/transactions', json={'amount': 100, 'category': 'food', 'user_id': 1})
        self.assertEqual(response.status_code, 201)

    def test_get_transactions(self):
        response = self.app.get('/transactions')
        self.assertEqual(response.status_code, 200)

    def test_convert_currency(self):
        response = self.app.get('/convert?amount=100&from=USD&to=EUR')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
