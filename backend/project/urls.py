from django.urls import path
from . import views
from .views import RecomendationView  # Make sure to import your class-based view

urlpatterns = [
    path('', views.index, name='index'),  # Main landing page
    path('form/', views.application_form, name='form'),  # Form page
    path('recommend/', views.get_recommendations, name='recommend'),  # Function-based API endpoint
    path('class-recommend/', RecomendationView.as_view(), name="class-recommend"),  # Class-based alternative
]
