import factory
import decimal
from factory.django import DjangoModelFactory
from main.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    
class ExpenseFactory(DjangoModelFactory):
    class Meta:
        model = Expense

    date = factory.Faker("date_time")
    name = factory.Faker("name")
    amount = factory.Faker("pydecimal", min_value=1, max_value=10000)
    category = factory.Iterator(Category.objects.all())
    is_fixed = factory.Faker("pybool")
    is_necessity = factory.Faker("pybool")
    user = factory.LazyFunction(lambda: User.objects.order_by("?").first() or UserFactory())
    
class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    description = factory.Faker("sentence", nb_words=15)
    user = factory.LazyFunction(lambda: User.objects.order_by("?").first() or UserFactory())
    
class IncomeFactory(DjangoModelFactory):
    class Meta:
        model = Income
    date = factory.Faker("date_time")
    name = factory.Faker("name")
    amount = factory.Faker("pydecimal", min_value=1, max_value=10000)
    user = factory.LazyFunction(lambda: User.objects.order_by("?").first() or UserFactory())


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal    
    name = factory.Faker("name")
    amount = factory.Faker("pydecimal", min_value=1, max_value=10000)
    saved = factory.Faker("pydecimal", min_value=1, max_value=10000)
    user = factory.LazyFunction(lambda: User.objects.order_by("?").first() or UserFactory())