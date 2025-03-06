from django.urls import path
from .views import *

urlpatterns = [
    path('v1/accounts/', ExpenseList.as_view()),
    path('v1/accounts/<int:pk>/', ExpenseDetailView.as_view()),
]