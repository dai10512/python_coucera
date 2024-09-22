from django.shortcuts import render
from django.http import HttpResponse
from . models import Menu
# Create your views here for menu.
def menu(response):
    menu_item = Menu.objects.all()
    items_dict = {
        'menu':menu_item
    }
    return render(response,'menu.html',items_dict)