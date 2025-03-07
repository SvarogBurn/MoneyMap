from django.urls import path
from .views import *

urlpatterns = [
    path('v1/expenses/', ExpenseList.as_view()),
    path('v1/expenses/<int:pk>/', ExpenseDetailView.as_view()),
]