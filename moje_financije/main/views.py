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

#------------------------Expenses--------------------------------
class ExpenseList(BaseListView):
    model = Expense
    search_fields = ['name', 'amount', 'date', 'is_fixed', 'is_necessity', 'category']
    template_name = 'main/expense_list.html'
    context_object_name = "expenses"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_month = now().month
        current_year = now().year

        expenses = Expense.objects.all()
        context['expenses'] = expenses
        
        total_spent = expenses.filter(date__month=current_month, date__year=current_year).aggregate(total=Sum('amount'))['total'] or 0
        context['total_spent'] = total_spent

        # Expenses by Category
        categories = Expense.objects.values('category').annotate(total_spent=Sum('amount'))
        for i in categories:
            i['name'] = Category.objects.get(pk=i['category']).name
        
        context['categories'] = categories
        print(categories)  

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

        current_month = now().month
        current_year = now().year

        incomes = Income.objects.all()
        context['incomes'] = incomes

        total_income = incomes.filter(date__month=current_month, date__year=current_year).aggregate(total=Sum('amount'))['total'] or 0
        context['total_income'] = total_income

        # Income by Source
        sources = Income.objects.values('name').annotate(total_earned=Sum('amount'))
        context['sources'] = sources

        # Total balance calculation
        total_expenses = Expense.objects.filter(date__month=current_month, date__year=current_year).aggregate(total=Sum('amount'))['total'] or 0
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