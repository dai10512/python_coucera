from django.shortcuts import render
from rest_framework import generics
from . models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer

# Create your views here.


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']  # 順序
    filterset_fields = ['price', 'inventory']  # フィルター
    search_fields = ['title']  # 検索（部分一致）
