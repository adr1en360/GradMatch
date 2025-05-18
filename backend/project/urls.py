from django.urls import path
from .views import get_recommendations, application_form

urlpatterns = [
    path('', application_form, name='application_form'),
    path('recommend/', get_recommendations, name='recommend'),
]