from django.shortcuts import render
from django.http import HttpResponse
from .models import Menu
from .forms import BookingForm

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

def home(response):
    return HttpResponse('''Welcome to Little Lemon!''')

def about(response):
    return HttpResponse('''About us''')

def menu(response):
    menu_item = Menu.objects.all()
    items_dict = {'menu':menu_item}
    return render(response,'menu.html',items_dict)

def book(response):
    return HttpResponse('''Make a booking''')

def form_view(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form" : form}
    return render(request, "booking.html", context)