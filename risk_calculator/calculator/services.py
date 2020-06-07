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
            apolicy = base_risk + 1
        else:
            apolicy = base_risk
    else:
        apolicy = None

    return apolicy

def calculate_disability_risk(base_risk, income, age, house, dependents, marital_status):
    if income == 0 or age > 60:
        apolicy = None
    else:
        apolicy = base_risk

        try:
            if house['ownership_status'] == 'mortgaged':
                apolicy += 1
        except (TypeError, KeyError):
                pass

        if dependents > 0:
            apolicy += 1

        if marital_status == 'married':
            apolicy -= 1

        if apolicy < 0:
            apolicy = 0

    return apolicy

def calculate_home_risk(base_risk, house):
    if house['ownership_status'] == 'mortgaged':
        apolicy = base_risk + 1
    elif house['ownership_status'] == 'owned':
        apolicy = base_risk
    else:
        apolicy = None

    return apolicy

def calculate_life_risk(base_risk, age, dependents, marital_status):
    if age > 60:
        apolicy = None
    else:
        apolicy = base_risk

        if dependents > 0:
            apolicy += 1

        if marital_status == 'married':
            apolicy += 1

    return apolicy

def adapt_apolicy(apolicy):
    if apolicy == None:
        apolicy_type = INSURANCE_TYPE['INELIGIBLE']
    elif apolicy <= 0:
        apolicy_type = INSURANCE_TYPE['ECONOMIC']
    elif apolicy == 1 or apolicy == 2:
        apolicy_type = INSURANCE_TYPE['REGULAR']
    elif apolicy >= 3:
        apolicy_type = INSURANCE_TYPE['RESPONSIBLE']

    return apolicy_type

def calculate_apolicy(json_data):
    age = json_data['age']
    dependents = json_data['dependents']
    house = json_data.get('house', None)
    income = json_data['income']
    marital_status = json_data['marital_status']
    risk = sum(json_data['risk_questions'])
    vehicle = json_data.get('vehicle', None)

    base_risk = calculate_base_risk(risk, age, income)

    auto_apolicy = calculate_auto_risk(base_risk, vehicle)
    disability_apolicy = calculate_disability_risk(base_risk, income, age, house, dependents, marital_status)
    home_apolicy = calculate_home_risk(base_risk, house)
    life_apolicy = calculate_life_risk(base_risk, age, dependents, marital_status)

    response = {
        "base_risk": base_risk,
        "auto": adapt_apolicy(auto_apolicy),
        "disability": adapt_apolicy(disability_apolicy),
        "home": adapt_apolicy(home_apolicy),
        "life": adapt_apolicy(life_apolicy)
    }

    return response
