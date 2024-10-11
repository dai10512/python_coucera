from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price',
                  'category', 'featured', 'category_id']


class CartSerializer(serializers.ModelSerializer):
    foreign_key = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    foreign_key = OrderSerializer()
    foreign_key = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
