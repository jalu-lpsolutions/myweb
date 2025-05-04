from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Customer,Serial_number

admin.site.register(Customer)
admin.site.register(Serial_number)