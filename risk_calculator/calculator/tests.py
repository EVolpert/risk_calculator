from django.test import TestCase
from django.utils import timezone

from calculator.services import calculate_policy

# Create your tests here.
class BaseCalulatorTestCase(TestCase):
    def setUp(self):
        self.base_request_data = {
            'age': 35,
            'dependents': 2,
            'house': {'ownership_status': 'owned'},
            'income': 59000,
            'marital_status': 'married',
            'risk_questions': [0, 1, 0],
            'vehicle': {'year': 2018}
        }

    def test_ineligible_apolicies(self):
        ineligible_data = self.base_request_data
        ineligible_data['age'] = 61
        ineligible_data['income'] = 0
        ineligible_data.pop('vehicle')
        ineligible_data. pop('house')

        policy = calculate_policy(ineligible_data)

        expected_return = {
            'auto': 'ineligible',
            'disability': 'ineligible',
            'home': 'ineligible',
            'life': 'ineligible'
        }

        self.assertEqual(policy, expected_return)


class AutoPolicyTestCase(TestCase):
    def setUp(self):
        self.base_request_data = {
            'age': 35,
            'dependents': 2,
            'house': {'ownership_status': 'owned'},
            'income': 59000,
            'marital_status': 'married',
            'risk_questions': [0, 1, 0],
            'vehicle': {'year': 2018}
        }

    def test_regular_auto_policy(self):
        regular_data = self.base_request_data

        policy = calculate_policy(regular_data)

        self.assertEqual('regular', policy['auto'])

    def test_economic_auto_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 20
        economic_data['risk_questions'] = [0, 0, 0]
        economic_data['vehicle']['year'] = 1990

        policy = calculate_policy(economic_data)

        self.assertEqual('economic', policy['auto'])

    def test_responsible_auto_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 50
        economic_data['risk_questions'] = [1, 1, 1]
        economic_data['vehicle']['year'] = 2020

        policy = calculate_policy(economic_data)

        self.assertEqual('responsible', policy['auto'])

class DisabilityPolicyTestCase(TestCase):
    def setUp(self):
        self.base_request_data = {
            'age': 35,
            'dependents': 2,
            'house': {'ownership_status': 'owned'},
            'income': 59000,
            'marital_status': 'married',
            'risk_questions': [0, 1, 0],
            'vehicle': {'year': 2018}
        }

    def test_regular_disability_policy(self):
        regular_data = self.base_request_data
        regular_data['risk_questions'] = [1, 1, 0]

        policy = calculate_policy(regular_data)

        self.assertEqual('regular', policy['disability'])

    def test_economic_disability_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 20
        economic_data['risk_questions'] = [0, 0, 0]

        policy = calculate_policy(economic_data)

        self.assertEqual('economic', policy['disability'])

    def test_responsible_disability_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 50
        economic_data['risk_questions'] = [1, 1, 1]

        policy = calculate_policy(economic_data)

        self.assertEqual('responsible', policy['disability'])

class HomePolicyTestCase(TestCase):
    def setUp(self):
        self.base_request_data = {
            'age': 35,
            'dependents': 2,
            'house': {'ownership_status': 'mortgaged'},
            'income': 59000,
            'marital_status': 'married',
            'risk_questions': [0, 1, 0],
            'vehicle': {'year': 2018}
        }

    def test_regular_home_policy(self):
        regular_data = self.base_request_data
        regular_data['risk_questions'] = [1, 1, 0]

        policy = calculate_policy(regular_data)

        self.assertEqual('regular', policy['home'])

    def test_economic_home_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 20
        economic_data['house']['ownership_status'] = 'owned'
        economic_data['risk_questions'] = [0, 0, 0]

        policy = calculate_policy(economic_data)

        self.assertEqual('economic', policy['home'])

    def test_responsible_home_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 50
        economic_data['risk_questions'] = [1, 1, 1]

        policy = calculate_policy(economic_data)

        self.assertEqual('responsible', policy['home'])

class LifePolicyTestCase(TestCase):
    def setUp(self):
        self.base_request_data = {
            'age': 35,
            'dependents': 2,
            'house': {'ownership_status': 'mortgaged'},
            'income': 59000,
            'marital_status': 'married',
            'risk_questions': [0, 1, 0],
            'vehicle': {'year': 2018}
        }

    def test_regular_life_policy(self):
        regular_data = self.base_request_data
        regular_data['risk_questions'] = [1, 0, 0]

        policy = calculate_policy(regular_data)

        self.assertEqual('regular', policy['life'])

    def test_economic_life_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 20
        economic_data['dependents'] = 0
        economic_data['marital_status'] = 'single'
        economic_data['house']['ownership_status'] = 'owned'

        policy = calculate_policy(economic_data)

        self.assertEqual('economic', policy['life'])

    def test_responsible_life_policy(self):
        economic_data = self.base_request_data
        economic_data['age'] = 50
        economic_data['marital_status'] = 'single'
        economic_data['risk_questions'] = [1, 1, 1]

        policy = calculate_policy(economic_data)

        self.assertEqual('responsible', policy['life'])
