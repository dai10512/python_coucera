from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price',
                  'featured', 'category_id', 'category']


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_id', 'menuitem_id', 'menuitem',
                  'unit_price', 'quantity', 'unit_price', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'status': {'min_value': 0, 'max_value': 1}
        }


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    delivery_crew = UserSerializer(
        read_only=True, required=False)
    delivery_crew_id = serializers.IntegerField(
        write_only=True, required=False)

    order_items = OrderItemSerializer(many=True, required=False)
    order_items_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False)
    # ここでOrderItemSerializerを使用する

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['order_items']
