from django.urls import path
from . import views
from .views import RecommendationView  # Make sure to import your class-based view

urlpatterns = [
    path('', views.index, name='index'),  # Main landing page
    path('form/', views.application_form, name='form'),  # Form page
    path('recommend/', views.get_recommendations, name='recommend'),  # Function-based API endpoint
    path('recommend-view/', RecommendationView.as_view(), name="recommend-view"),  # Class-based alternative
]
