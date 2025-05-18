from django.urls import path
from . import views
from .views import RecommendationView  # Make sure to import your class-based view

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index'),
    path('form/', views.application_form, name='form'),
    path('recommend/', views.get_recommendations, name='recommend'),
    path('statement-editor/', views.statement_editor, name='statement_editor'),
    path('checklist/', views.checklist, name='checklist'),
    path('checklist/detail/', views.checklist_detail, name='checklist_detail'),
    path('forum/', views.forum, name='forum'),
    path('auth/', views.auth, name='auth'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
=======
    path('', views.index, name='index'),  # Main landing page
    path('form/', views.application_form, name='form'),  # Form page
    path('recommend/', views.get_recommendations, name='recommend'),  # Function-based API endpoint
    path('recommend-view/', RecommendationView.as_view(), name="recommend-view"),  # Class-based alternative
]
>>>>>>> origin/main
