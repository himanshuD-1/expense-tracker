from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from userincome.models import Source, UserIncome
from userpreferences.models import UserPreference
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url="/authentication/login")
def index(request):
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = None
        
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)

@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    
    context = {
        'sources': sources,
        'values': request.POST
    }

    if request.method == "GET":
        return render(request, 'income/add-income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'income/add-income.html', context)

        if not description:
            messages.error(request, "Description is required")
            return render(request, 'income/add-income.html', context)

    UserIncome.objects.create(owner=request.user, amount=amount,
                           description=description, date=date, source=source)
    messages.success(request, "Income added successfully..!!")
    return redirect('income')

@login_required(login_url="/authentication/login")
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    source = Source.objects.all()

    context = {
        'income': income,
        'values': income,
        'sources': source,
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)

    if request.method == 'POST':
        if request.method == 'POST':
            amount = request.POST['amount']
            description = request.POST['description']
            source = request.POST['source']
            date = request.POST['date']

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'income/add-income.html', context)

        if not description:
            messages.error(request, "Description is required")
            return render(request, 'income/add-income.html', context)

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.category = source
        income.description = description

        income.save()
        messages.success(request, "Income Updated Successfully")
        return redirect("income")

@login_required(login_url="/authentication/login") 
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income Removed..!!")

    return redirect('income')