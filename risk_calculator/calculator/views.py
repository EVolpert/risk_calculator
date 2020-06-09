import json
from json import JSONDecodeError

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.middleware.csrf import get_token

from calculator.services import calculate_policy
from calculator.validators import request_validator

class PolicyCalculator(View):
    def post(self, request):
        try:
            request_data=json.loads(request.body)
        except JSONDecodeError:
            response = HttpResponse('Error Decoding Json' ,status=400)
        else:
            valid_data, error_message = request_validator(request_data)
            if valid_data:
                policy = calculate_policy(request_data)
                response = JsonResponse(policy)
            else:
                message = error_message
                response = HttpResponse(error_message, status=400)

        return response

class getCRSFTOKEN(View):
    def get(self, request):
        return HttpResponse(get_token(request))
