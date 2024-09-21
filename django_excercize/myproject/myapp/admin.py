from django.contrib import admin
from .models import Booking, Employees,DrinksCategory,Drinks

# Register your models here.
admin.site.register(Drinks)
admin.site.register(DrinksCategory)
admin.site.register(Booking)
admin.site.register(Employees)