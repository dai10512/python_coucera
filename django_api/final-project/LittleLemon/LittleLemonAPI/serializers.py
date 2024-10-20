from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
    user = UserSerializer()
    menuitem = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = ['user', 'quantity', 'menuitem', 'price', 'unit_price']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'status': {'min_value': 0, 'max_value': 1}
        }


class OrderSerializer(serializers.ModelSerializer):
    delivery_crew = UserSerializer(required=False)
    order_items = OrderItemSerializer(many=True, required=False)
    # ここでOrderItemSerializerを使用する

    class Meta:
        model = Order
        fields = ['status', 'date', 'delivery_crew',
                  'total', 'user', 'order_items']
        read_only_fields = ['order_items']
