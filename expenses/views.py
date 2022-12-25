from datetime import datetime, timedelta
from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import json
from expenses.models import Category, Expense
from django.http import JsonResponse,HttpResponse
import csv
from userpreferences.models import UserPreference
# Create your views here.


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expense = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__startswith=search_str, owner=request.user) | Expense.objects.filter(
            category__startswith=search_str, owner=request.user)

        data = expense.values()
        return JsonResponse(list(data),safe=False)
        
@login_required(login_url="/authentication/login")
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = None
        
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url="/authentication/login")
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }

    if request.method == "GET":
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expenses.html', context)

    Expense.objects.create(owner=request.user, amount=amount,
                           description=description, date=date, category=category)
    messages.success(request, "Expense added successfully..!!")
    return redirect('expenses')

@login_required(login_url="/authentication/login")
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()

    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expenses.html', context)

    if request.method == 'POST':
        if request.method == 'POST':
            amount = request.POST['amount']
            description = request.POST['description']
            category = request.POST['category']
            date = request.POST['date']

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expenses.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, "Expenses Updated Successfully")
        return redirect("expenses")

@login_required(login_url="/authentication/login") 
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense Removed..!!")

    return redirect('expenses')


def expense_category_summary(request):
    todays_date =date.today()
    six_month_ago = todays_date - timedelta(days=30*6)
    expenses= Expense.objects.filter(owner= request.user, date__gte = six_month_ago, date__lte=todays_date)
    finalrep={}
    
   
    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category,expenses)))
    
    def expense_category_amount(category):
        amount = 0
        filter_by_category= Expense.objects.filter(category= category)
        
        for item in filter_by_category:
            amount += item.amount
            
        return amount
    
    for x in expenses:
        for y in category_list:
            finalrep[y] = expense_category_amount(y)
    
    return JsonResponse({'expense_category_data':finalrep},safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')
  
  
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filenamme = Expenses'+ str(datetime.now())+'.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    
    expenses = Expense.objects.filter(owner=request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])
        
    return response
         