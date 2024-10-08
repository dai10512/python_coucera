from .models import MenuItem, Order
from .serializers import MenuItemSerializer, OrderSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics

# Create your views here.


class UsersView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class UsersUsersMeView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class TokenLoginView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemsSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class GroupsManagerUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupsManagerUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupsDeliveryCrewUsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupsDeliveryCrewUsersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CartMenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class OrdersView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrdersSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializes_class = OrderSerializer
