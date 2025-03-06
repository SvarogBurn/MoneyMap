from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('expense-tracker/', ExpenseList.as_view(), name='expense_list'),
    path('budget-breakdown/', IncomeList.as_view(), name='income_list'),
    path('saving-goals/', GoalList.as_view(), name='goal_list'),
    path('', views.index, name='index'),
    path('register/', register, name='register'),
]

