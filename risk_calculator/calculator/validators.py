MARITAL_STATUS = ['single', 'married']
HOUSE_STATUS = ['owned', 'mortgaged']

def vehicle_validator(vehicle_data):
    valid = True
    if vehicle_data:
        if 'year' not in vehicle_data:
            valid = False
        else:
            if vehicle_data['year'] < 1886:
                valid = False
    return valid

def house_validator(house_data):
    valid = True
    if house_data:
        if 'ownership_status' not in house_data:
            valid = False
        else:
            if house_data['ownership_status'] not in HOUSE_STATUS:
                valid = False
    return valid

def risk_questions_validator(risk_questions_data):
    valid = True

    if len(risk_questions_data) != 3:
        valid = False
    else:
        for value in risk_questions_data:
            if value == 0 or value == 1:
                pass
            else:
                valid = False
                break
    return valid

def marital_status_validator(marital_status_data):
    valid = True
    if marital_status_data not in MARITAL_STATUS:
        valid = False

    return valid

def numeric_field_validator(field_data):
    valid = True
    if isinstance(field_data, int):
        if field_data < 0:
            valid = False
    else:
        valid = False

    return valid

def validate_format_data(request_data):
    expected_fields = ['age', 'dependents', 'income', 'marital_status', 'risk_questions', 'house', 'vehicle']
    missing_fields = []
    for field in expected_fields:
        try:
            request_data[field]
        except KeyError as error:
            missing_fields.append(error.args[0])
    else:
        if len(missing_fields) > 0:
            valid = False
        else:
            valid = True
    return valid, missing_fields

def request_validator(request_data):
    error_message = ''
    valid_format, missing_fields = validate_format_data(request_data)

    if valid_format:
        valid = True

        age_validation = numeric_field_validator(request_data['age'])
        income_validation = numeric_field_validator(request_data['income'])
        dependents_validation = numeric_field_validator(request_data['dependents'])
        marital_status_validation = marital_status_validator(request_data['marital_status'])
        risk_question_validation = risk_questions_validator(request_data['risk_questions'])
        house_validation = house_validator(request_data['house'])
        vehicle_validaton = vehicle_validator(request_data['vehicle'])

        if not age_validation:
            error_message += f'Invalid age value/n'
        if not income_validation:
            error_message += f'Invalid income value/n'
        if not dependents_validation:
            error_message += f'Invalid dependents value/n'
        if not marital_status_validation:
            error_message += f'Invalid marital status value/n'
        if not risk_question_validation:
            error_message += f'Invalid risk question value/n'
        if not house_validation:
            error_message += f'Invalid house validation value/n'
        if not vehicle_validaton:
            error_message += f'Invalid vehicle value/n'

        if len(error_message) > 0:
            valid = False
    else:
        valid = False
        error_message += f'Invalid Format. Missing: {missing_fields} fields'

    return valid, error_message
