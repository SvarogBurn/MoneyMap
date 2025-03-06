from django.urls import path
from .views import *
from . import views

expense_views = [
    path('expense-tracker/', ExpenseList.as_view(), name='expense_list'),
    path('expense-tracker/<int:pk>/', ExpenseDetail.as_view(), name='expense_detail'),
    path('expense-tracker/create/', ExpenseCreate.as_view(), name='expense_create'),
    path('expense-tracker/<int:pk>/update/', ExpenseUpdate.as_view(), name='expense_update'),
    path('expense-tracker/<int:pk>/delete/', ExpenseDelete.as_view(), name='expense_delete'),
    ]

income_views = [
    path('budget-breakdown/', IncomeList.as_view(), name='income_list'),
    path('budget-breakdown/<int:pk>/', IncomeDetail.as_view(), name='income_detail'),
    path('budget-breakdown/create/', IncomeCreate.as_view(), name='income_create'),
    path('budget-breakdown/<int:pk>/update/', IncomeUpdate.as_view(), name='income_update'),
    path('budget-breakdown/<int:pk>/delete/', IncomeDelete.as_view(), name='income_delete'),
    ]

goal_views = [
    path('saving-goals/', GoalList.as_view(), name='goal_list'),
    path('saving-goals/<int:pk>/', GoalDetail.as_view(), name='goal_detail'),
    path('saving-goals/create/', GoalCreate.as_view(), name='goal_create'),
    path('saving-goals/<int:pk>/update/', GoalUpdate.as_view(), name='goal_update'),
    path('saving-goals/<int:pk>/delete/', GoalDelete.as_view(), name='goal_delete'),
    ]

urlpatterns = [
    *expense_views, 
    *income_views, 
    *goal_views, 
    path('', views.index, name='index'),
    path('register/', register, name='register'),
]

