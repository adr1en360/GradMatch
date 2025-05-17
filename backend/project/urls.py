from django.urls import path
from .views import *

urlpatterns = [
    path("recommend/", RecomendationView.as_view(), name="recommend"),
]