import random

from django.db import transaction
from django.core.management.base import BaseCommand

from main.models import *
from main.factories import *

NUM_EXPENSES = 200
NUM_CATEGORIES = 5
NUM_INCOMES = 200
NUM_GOALS = 5
NUM_USERS = 10


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [Expense, Category, Income, Expense]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_USERS):
            expense = UserFactory()
        for _ in range(NUM_CATEGORIES):
            category = CategoryFactory()
        for _ in range(NUM_EXPENSES):
            expense = ExpenseFactory()
        for _ in range(NUM_INCOMES):
            transaction = IncomeFactory()
        for _ in range(NUM_GOALS):
            transaction = GoalFactory()