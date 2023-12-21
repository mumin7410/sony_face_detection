from django.contrib import admin
from .models import Member, EmployeeInfo, Transaction

# Register your models here.
admin.site.register(Member)
admin.site.register(EmployeeInfo)
admin.site.register(Transaction)


