import factory
import decimal
from factory.django import DjangoModelFactory
from main.models import *

class ExpensesFactory(DjangoModelFactory):
    class Meta:
        model = Expense


    date = factory.Faker("date_time")
    name = factory.Faker("expense_name")
    amount = factory.Faker("pydecimal", min_value=1, max_value=10000)
    category = factory.Iterator(Category.objects.all())
    is_fixed = factory.Faker("pybool")
    is_necessary = factory.Faker("pybool")
    #user?
    
    
    last_name = factory.Faker("last_name")
    iban = factory.Faker("pystr", max_chars=21)
    balance = factory.Faker("pydecimal", min_value=1, max_value=10000)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    description = factory.Faker("sentence", nb_words=15)
    #user?
    

class IncomeFactory(DjangoModelFactory):
    class Meta:
        model = Income
    date = factory.Faker("date_time")
    name = factory.Faker("expense_name")
    amount = factory.Faker("pydecimal", min_value=1, max_value=10000)
    #user



class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal    
    name = factory.Faker("expense_name")
    amount = factory.Faker("pydecimal", min_value=1, max_value=10000)
    saved = factory.Faker("pydecimal", min_value=1, max_value=10000)
    #user?