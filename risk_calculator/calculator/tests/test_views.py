import json

from django.test import TestCase, Client
from django.utils import timezone

from calculator.validators import request_validator

class PolicyCalculatorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_request_data = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 1,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 1900}
        }

    def test_valid_response(self):
        data = json.dumps(self.base_request_data)
        response = self.client.post('/calculator/risk', data, content_type="application/json")

        response_data = json.loads(response.content)
        self.assertEqual(response_data, {"auto": "economic", "disability": "economic", "home": "economic", "life": "regular"})
        self.assertEqual(response.status_code, 200)

    def test_invalid_response_invalid_data(self):
        data = self.base_request_data
        data.pop('age')
        json_data = json.dumps(data)
        response = self.client.post('/calculator/risk', json_data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
