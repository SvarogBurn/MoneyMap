from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Expense, Income, Goal

class ExpenseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.expense = Expense.objects.create(
            name="Test Expense",
            amount=100.00,
            date="2024-03-06",
            is_fixed=True,
            is_necessary=True,
            category="Food"
        )

    def test_expense_list_view(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Expense")

    def test_expense_detail_view(self):
        response = self.client.get(reverse('expense_detail', args=[self.expense.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Expense")

    def test_expense_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('expense_create'), {
            'name': 'New Expense',
            'amount': 50.00,
            'date': '2024-03-06',
            'is_fixed': False,
            'is_necessary': True,
            'category': 'Transport'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Expense.objects.count(), 2)

    def test_expense_update_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('expense_update', args=[self.expense.pk]), {
            'name': 'Updated Expense',
            'amount': 120.00,
            'date': '2024-03-06',
            'is_fixed': True,
            'is_necessary': False,
            'category': 'Entertainment'
        })
        self.assertEqual(response.status_code, 302)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.name, "Updated Expense")

    def test_expense_delete_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('expense_delete', args=[self.expense.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(pk=self.expense.pk).exists())

class AuthenticationTests(TestCase):
    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'Testpass123',
            'password2': 'Testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        User.objects.create_user(username='testuser', password='password')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302)  # Redirect after login
