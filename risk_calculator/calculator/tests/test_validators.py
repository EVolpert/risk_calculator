from django.test import TestCase
from django.utils import timezone

from calculator.validators import request_validator

class DataValidatorFormatTestCase(TestCase):
    def setUp(self):
        self.base_request_data = {
            'age': 35,
            'dependents': 2,
            'house': {'ownership_status': 'owned'},
            'income': 0,
            'marital_status': 'married',
            'risk_questions': [0, 1, 0],
            'vehicle': {'year': 2018}
        }

    def test_missing_required_field(self):
        missing_one_required_field = self.base_request_data
        missing_one_required_field.pop('age')

        valid, error_message = request_validator(missing_one_required_field)
        self.assertFalse(valid)
        self.assertEqual("Invalid Format. Missing: ['age'] fields", error_message)

    def test_missing_non_required_field(self):
        missing_non_required_field = self.base_request_data
        missing_non_required_field.pop('house')

        valid, error_message = request_validator(missing_non_required_field)
        self.assertFalse(valid)
        self.assertEqual("Invalid Format. Missing: ['house'] fields", error_message)

    def test_missing_multiple_fields(self):
        missing_multiple_fields =  self.base_request_data
        missing_multiple_fields.pop('income')
        missing_multiple_fields.pop('vehicle')
        missing_multiple_fields.pop('risk_questions')

        valid, error_message = request_validator(missing_multiple_fields)
        self.assertFalse(valid)
        self.assertEqual("Invalid Format. Missing: ['income', 'risk_questions', 'vehicle'] fields", error_message)

    def test_non_required_field_blank(self):
        non_required_field_blank = self.base_request_data
        non_required_field_blank['house'] = {}
        non_required_field_blank['vehicle'] = {}

        valid, error_message = request_validator(non_required_field_blank)
        self.assertTrue(valid)
        self.assertFalse(error_message)

    def test_valid_request(self):
        valid, error_message = request_validator(self.base_request_data)

        self.assertTrue(valid)
        self.assertFalse(error_message)

    def test_valid_format_invalid_value(self):
        invalid_values = self.base_request_data
        invalid_values['income'] = -10
        invalid_values['risk_questions'] = [2, -1, 0]
        invalid_values['vehicle']['year'] = 1500

        valid, error_message = request_validator(invalid_values)
        self.assertFalse(valid)
        self.assertEqual('Invalid income value/nInvalid risk question value/nInvalid vehicle value/n', error_message)
