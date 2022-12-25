from django.contrib import admin

from userincome.models import Source, UserIncome

# Register your models here.
admin.site.register(UserIncome)
admin.site.register(Source)