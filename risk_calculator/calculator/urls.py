from django.urls import path

from calculator import views

urlpatterns = [
    path('risk', views.PolicyCalculator.as_view()),
    path('crsf', views.getCRSFTOKEN.as_view())
]
