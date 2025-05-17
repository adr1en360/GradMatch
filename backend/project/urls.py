from django.urls import path
from .views import *

urlpatterns = [
    path("execute-flow/", LangflowExecuteView.as_view(), name="execute_flow"),
]