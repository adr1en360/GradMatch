from django.urls import path
from . import views

urlpatterns = [
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