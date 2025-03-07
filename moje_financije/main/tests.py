from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Expense, Income, Goal, Category
from django.utils.timezone import now

class ExpenseViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Food', user=self.user)
        self.expense = Expense.objects.create(
            date=now(), name='Groceries', amount=50.00, category=self.category, user=self.user, is_fixed=True, is_necessity=True
        )

    def test_expense_list_view(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/expense_list.html')

    def test_expense_detail_view(self):
        response = self.client.get(reverse('expense_detail', args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/expense_detail.html')

    def test_expense_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('expense_create'), {
            'date': now(), 'name': 'Transport', 'amount': 20.00, 'category': self.category.id, 'is_fixed': False, 'is_necessity': True
        })
        self.assertEqual(response.status_code, 302)

    def test_expense_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('expense_update', args=[self.expense.id]), {
            'date': now(), 'name': 'Groceries Updated', 'amount': 60.00, 'category': self.category.id, 'is_fixed': True, 'is_necessity': True
        })
        self.assertEqual(response.status_code, 302)

    def test_expense_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('expense_delete', args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)


class IncomeViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.income = Income.objects.create(date=now(), name='Salary', amount=1000.00, user=self.user)

    def test_income_list_view(self):
        response = self.client.get(reverse('income_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/income_list.html')

    def test_income_detail_view(self):
        response = self.client.get(reverse('income_detail', args=[self.income.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/income_detail.html')

    def test_income_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('income_create'), {
            'date': now(), 'name': 'Bonus', 'amount': 500.00
        })
        self.assertEqual(response.status_code, 302)

    def test_income_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('income_update', args=[self.income.id]), {
            'date': now(), 'name': 'Salary Updated', 'amount': 1200.00
        })
        self.assertEqual(response.status_code, 302)

    def test_income_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('income_delete', args=[self.income.id]))
        self.assertEqual(response.status_code, 302)


class GoalViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.goal = Goal.objects.create(name='Vacation', amount=2000.00, saved=500.00, user=self.user)

    def test_goal_list_view(self):
        response = self.client.get(reverse('goal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/goal_list.html')

    def test_goal_detail_view(self):
        response = self.client.get(reverse('goal_detail', args=[self.goal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/goal_detail.html')

    def test_goal_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('goal_create'), {
            'name': 'Car', 'amount': 15000.00, 'saved': 2000.00
        })
        self.assertEqual(response.status_code, 302)

    def test_goal_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('goal_update', args=[self.goal.id]), {
            'name': 'Vacation Updated', 'amount': 2500.00, 'saved': 600.00
        })
        self.assertEqual(response.status_code, 302)

    def test_goal_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('goal_delete', args=[self.goal.id]))
        self.assertEqual(response.status_code, 302)
