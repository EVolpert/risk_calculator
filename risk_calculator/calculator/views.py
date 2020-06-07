import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.middleware.csrf import get_token

from calculator.services import calculate_policy

class RiskCalculator(View):
    def post(self, request):
        try:
            request_data=json.loads(request.body)
        except JSONDecodeError :
            request_data = None

        response = calculate_policy(request_data)

        return JsonResponse(response)

class getCRSFTOKEN(View):
    def get(self, request):
        return HttpResponse(get_token(request))
