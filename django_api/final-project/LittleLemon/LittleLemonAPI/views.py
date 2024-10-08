from django.http import response
from .models import MenuItem, Order


# Create your views here.
class MenuItemsView(response):
    queryset = MenuItem.objects.all()
    # serializer_class = MenuItemSerializer


class SingleMenuItemView(response):
    queryset = MenuItem.objects.all()
    # serializer_class = MenuItemSerializer


class CartMenuItemsView(response):
    queryset = MenuItem.objects.all()
    # serializer_class = MenuItemSerializer


class OrdersView(response):
    queryset = Order.objects.all()
    # serializer_class = MenuItemSerializer


class SingleOrdersView(response):
    queryset = Order.objects.all()
