from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def drinks(request,drink_name):
    drinkDic = {
        'mocha':'type of coffee',
        'tea':'type of beverage',
        'lemonade' : 'type of refreshment',
    }
    choice_of_drink = drinkDic[drink_name]
    title = f"<h2> {drink_name} </h2>"
    return HttpResponse(f"<h2>{drink_name}</h2> " + choice_of_drink)