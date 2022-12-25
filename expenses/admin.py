
from django.contrib import admin

from expenses.models import Category, Expense

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display=('amount','description','owner','category','date')
    search_fields=('description','category','date')
    
admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Category)