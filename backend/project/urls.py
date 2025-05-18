from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.application_form, name='form'),
    path('recommend/', views.get_recommendations, name='recommend'),
]