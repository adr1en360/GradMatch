from django.urls import path
from .views import *

urlpatterns = [
    path('', RecomendationView.as_view(), name="recommend"),
]