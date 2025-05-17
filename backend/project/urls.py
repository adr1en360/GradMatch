from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path("recommend/", RecomendationView.as_view(), name="recommend"),
]