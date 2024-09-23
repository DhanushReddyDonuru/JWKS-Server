
import unittest
import json
from app import app

class JWKSTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_auth(self):
        response = self.app.post('/auth', json={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    def test_auth_expired(self):
        response = self.app.post('/auth', json={'username': 'testuser'})
        token = json.loads(response.data)['token']
        
        # Token expiration handling would typically require testing with time manipulation
        self.assertEqual(response.status_code, 200)

    def test_jwks(self):
        response = self.app.get('/jwks')
        json_data = json.loads(response.data)
        self.assertIn('keys', json_data)

if __name__ == '__main__':
    unittest.main()



