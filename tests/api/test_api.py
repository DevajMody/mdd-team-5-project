from flask import Flask, request
from unittest import TestCase
from unittest.mock import patch
from src.api.homework_tracker_api import SignUp 
from src.db.homework_tracker_db import rebuild_tables

app = Flask(__name__)
rebuild_tables()

app.config['TESTING'] = True

class TestSignupFunctionality(TestCase):

    @patch('src.db.homework_tracker_db.signup') 
    def test_signup(self, mock_signup):
        mock_signup.return_value = 1  
        signup_resource = SignUp()
    
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }

        with app.test_request_context('/signup', method='POST', json=data):
            with patch('flask.request.get_json', return_value=data): 
                response = signup_resource.post()

                self.assertEqual(response[0]['user_id'], 1) 
