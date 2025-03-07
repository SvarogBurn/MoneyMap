from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main.models import Expense, Income, Goal, Category
from django.db.models import Sum
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
#------------------------Mixin for Filtering--------------------------------
class SearchMixin:
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')

        if search_query and self.search_fields:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(query)
            
        return queryset

#------------------------Base Views--------------------------------
class BaseListView(SearchMixin, ListView):
    pass

class BaseDetailView(DetailView):
    pass

class BaseCRUDView(LoginRequiredMixin):
    def get_success_url(self):
        return reverse_lazy(f"{self.model.__name__.lower()}_detail", kwargs={'pk': self.object.pk})

class BaseCreateView(BaseCRUDView, CreateView):
    pass

class BaseUpdateView(BaseCRUDView, UpdateView):
    pass

class BaseDeleteView(LoginRequiredMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy(f"{self.model.__name__.lower()}_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model.__name__.lower()  # Pass model name to the template
        return context


#------------------------Expenses--------------------------------
class ExpenseList(BaseListView):
    model = Expense
    search_fields = ['name', 'amount', 'date', 'is_fixed', 'is_necessity', 'category']
    template_name = 'main/expense_list.html'
    context_object_name = "expenses"

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)

        category = self.request.GET.get('category')
        is_fixed = self.request.GET.get('fixed_variable')
        is_necessity = self.request.GET.get('necessity')
        min_amount = self.request.GET.get('min_amount')
        max_amount = self.request.GET.get('max_amount')
        search_name = self.request.GET.get('name')
        
        # Apply filters if parameters exist
        if category:
            queryset = queryset.filter(category__name=category)

        if is_fixed in ['Fixed', 'Variable']:
            queryset = queryset.filter(is_fixed=(is_fixed == 'Fixed'))

        if is_necessity in ['Need', 'Want']:
            queryset = queryset.filter(is_necessity=(is_necessity == 'Need'))

        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        if search_name:
            queryset = queryset.filter(name__icontains=search_name)
            
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Pass categories for filtering dropdown
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_month = now().month
        current_year = now().year

        expenses = self.object_list
        context['expenses'] = expenses
        
        total_spent = expenses.filter(user=self.request.user).aggregate(total=Sum('amount'))['total'] or 0
        context['total_spent'] = total_spent

        # Expenses by Category
        included_categories = { e.category.name for e in expenses }
        print(included_categories)
        categories = Expense.objects.filter(category__name__in=included_categories).values('category').annotate(total_spent=Sum('amount'))
        for i in categories:
            i['name'] = Category.objects.get(pk=i['category']).name

        context['categories'] = categories
        context['all_categories'] = Category.objects.all()

        # Wants vs. Needs
        wants_total = expenses.filter(is_necessity=False).aggregate(total=Sum('amount'))['total'] or 0
        needs_total = expenses.filter(is_necessity=True).aggregate(total=Sum('amount'))['total'] or 0
        context['wants_vs_needs'] = {'Wants': wants_total, 'Needs': needs_total}

        # Fixed vs. Variable
        fixed_total = expenses.filter(is_fixed=True).aggregate(total=Sum('amount'))['total'] or 0
        variable_total = expenses.filter(is_fixed=False).aggregate(total=Sum('amount'))['total'] or 0
        context['fixed_vs_variable'] = {'Fixed': fixed_total, 'Variable': variable_total}

        return context
    
class ExpenseDetail(BaseDetailView):
    model = Expense
    template_name = 'main/expense_detail.html'

class ExpenseCreate(BaseCreateView):
    model = Expense
    fields = ['date', 'name', 'amount', 'category', 'is_fixed', 'is_necessity']
    template_name = 'main/expense_form.html'

class ExpenseUpdate(BaseUpdateView):
    model = Expense
    fields = ['date', 'name', 'amount', 'category', 'is_fixed', 'is_necessity']
    template_name = 'main/expense_form.html'

class ExpenseDelete(BaseDeleteView):
    model = Expense
    template_name = 'main/object_confirm_delete.html'

#------------------------Income--------------------------------
class IncomeList(BaseListView):
    model = Income
    template_name = 'main/income_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        incomes = Income.objects.filter(user=self.request.user)
        context['incomes'] = incomes

        total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
        context['total_income'] = total_income

        # Income grouped by month
        monthly_income = (
            incomes.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total_earned=Sum('amount'))
            .order_by('month')
        )
        context['monthly_income'] = monthly_income

        # Total balance calculation
        total_expenses = Expense.objects.filter(user=self.request.user).aggregate(total=Sum('amount'))['total'] or 0
        context['remaining_balance'] = total_income - total_expenses

        return context
    

class IncomeDetail(BaseDetailView):
    model = Income
    template_name = 'main/income_detail.html'

class IncomeCreate(BaseCreateView):
    model = Income
    fields = ['date', 'name', 'amount']
    template_name = 'main/income_form.html'

class IncomeUpdate(BaseUpdateView):
    model = Income
    fields = ['date', 'name', 'amount']
    template_name = 'main/income_form.html'

class IncomeDelete(BaseDeleteView):
    model = Income
    template_name = 'main/object_confirm_delete.html'

#------------------------Goals--------------------------------
class GoalList(BaseListView):
    model = Goal
    template_name = 'main/goal_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goals'] = Goal.objects.filter(user=self.request.user)
        
        # Add dynamically calculated field for each goal
        for goal in context['goals']:
            goal.amount_left = max(goal.amount - goal.saved, 0)

        return context

class GoalDetail(BaseDetailView):
    model = Goal
    template_name = 'main/goal_detail.html'

class GoalCreate(BaseCreateView):
    model = Goal
    fields = ['name', 'amount', 'saved']
    template_name = 'main/goal_form.html'

class GoalUpdate(BaseUpdateView):
    model = Goal
    fields = ['name', 'amount', 'saved']
    template_name = 'main/goal_form.html'

class GoalDelete(BaseDeleteView):
    model = Goal
    template_name = 'main/object_confirm_delete.html'

#------------------------Authentication--------------------------------
def index(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})