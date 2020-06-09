from django.utils import timezone

INSURANCE_TYPE = {
    'INELIGIBLE': 'ineligible',
    'REGULAR': 'regular',
    'ECONOMIC': 'economic',
    'RESPONSIBLE': 'responsible'
}

def calculate_base_risk(risk, age, income):
    base_risk = risk

    if age < 30:
        base_risk -= 2
    elif 30 <= age <= 40:
        base_risk -= 1

    if income > 200000:
        base_risk -= 1

    if base_risk < 0:
        base_risk = 0

    return base_risk

def calculate_auto_risk(base_risk, vehicle):
    if vehicle:
        if timezone.now().year - vehicle['year'] <= 5:
            policy = base_risk + 1
        else:
            policy = base_risk
    else:
        policy = None

    return policy

def calculate_disability_risk(base_risk, income, age, house, dependents, marital_status):
    if income == 0 or age > 60:
        policy = None
    else:
        policy = base_risk

        try:
            if house['ownership_status'] == 'mortgaged':
                policy += 1
        except (TypeError, KeyError):
                pass

        if dependents > 0:
            policy += 1

        if marital_status == 'married':
            policy -= 1

        if policy < 0:
            policy = 0

    return policy

def calculate_home_risk(base_risk, house):
    if house:
        if house['ownership_status'] == 'mortgaged':
            policy = base_risk + 1
        elif house['ownership_status'] == 'owned':
            policy = base_risk
    else:
        policy = None

    return policy

def calculate_life_risk(base_risk, age, dependents, marital_status):
    if age > 60:
        policy = None
    else:
        policy = base_risk

        if dependents > 0:
            policy += 1

        if marital_status == 'married':
            policy += 1

    return policy

def adapt_policy(policy):
    if policy == None:
        policy_type = INSURANCE_TYPE['INELIGIBLE']
    elif policy <= 0:
        policy_type = INSURANCE_TYPE['ECONOMIC']
    elif policy == 1 or policy == 2:
        policy_type = INSURANCE_TYPE['REGULAR']
    elif policy >= 3:
        policy_type = INSURANCE_TYPE['RESPONSIBLE']

    return policy_type

def calculate_policy(json_data):
    age = json_data['age']
    dependents = json_data['dependents']
    house = json_data.get('house', None)
    income = json_data['income']
    marital_status = json_data['marital_status']
    risk = sum(json_data['risk_questions'])
    vehicle = json_data.get('vehicle', None)

    base_risk = calculate_base_risk(risk, age, income)

    auto_policy = calculate_auto_risk(base_risk, vehicle)
    disability_policy = calculate_disability_risk(base_risk, income, age, house, dependents, marital_status)
    home_policy = calculate_home_risk(base_risk, house)
    life_policy = calculate_life_risk(base_risk, age, dependents, marital_status)

    response = {
        'auto': adapt_policy(auto_policy),
        'disability': adapt_policy(disability_policy),
        'home': adapt_policy(home_policy),
        'life': adapt_policy(life_policy)
    }

    return response
