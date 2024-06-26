import unittest
from app import app, db
from models import User, Transaction

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_add_user(self):
        response = self.app.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 201)

    def test_add_transaction(self):
        self.app.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
        response = self.app.post('/transactions', json={'amount': 100.0, 'category': 'Food', 'user_id': 1})
        self.assertEqual(response.status_code, 201)

    def test_get_transactions(self):
        response = self.app.get('/transactions')
        self.assertEqual(response.status_code, 200)

    def test_update_transaction(self):
        self.app.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
        self.app.post('/transactions', json={'amount': 100.0, 'category': 'Food', 'user_id': 1})
        response = self.app.put('/transactions/1', json={'amount': 150.0, 'category': 'Groceries'})
        self.assertEqual(response.status_code, 200)

    def test_delete_transaction(self):
        self.app.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
        self.app.post('/transactions', json={'amount': 100.0, 'category': 'Food', 'user_id': 1})
        response = self.app.delete('/transactions/1')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
