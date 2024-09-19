from django.contrib import admin
from .models import Drinks
from .models import DrinksCategory

# Register your models here.
admin.site.register(Drinks)
admin.site.register(DrinksCategory)