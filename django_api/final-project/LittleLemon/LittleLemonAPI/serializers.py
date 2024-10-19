from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User
from datetime import datetime


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
    user = UserSerializer(read_only=True)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'quantity', 'menuitem', 'price', 'unit_price']

    def create(self, validated_data):
        user = self.context['request'].user
        menuitem = validated_data.get('menuitem')
        try:
            cart_item = Cart.objects.get(user=user, menuitem=menuitem)
            cart_item.quantity += validated_data.get('quantity')
            cart_item.unit_price = self.calculate_unit_price(validated_data)
            cart_item.price = self.calculate_price(validated_data)
            cart_item.save()
            return cart_item
        except Cart.DoesNotExist:
            validated_data['user'] = user
            validated_data['unit_price'] = self.calculate_unit_price(
                validated_data)
            validated_data['price'] = self.calculate_price(validated_data)
            return super().create(validated_data)

    def calculate_unit_price(self, validated_data):
        # `unit_price`を計算する具体的なロジック
        menuitem = validated_data.get('menuitem')
        calculated_value = menuitem.price  # 例としてメニューアイテムの価格をそのまま使用
        return calculated_value

    def calculate_price(self, validated_data):
        # `price`を計算する具体的なロジック
        unit_price = self.calculate_unit_price(validated_data)
        quantity = validated_data.get('quantity')
        calculated_value = unit_price * quantity
        return calculated_value


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    # ここでOrderItemSerializerを使用する

    class Meta:
        model = Order
        fields = ['status', 'date', 'delivery_crew',
                  'total', 'user']
        read_only_fields = ['status', 'date',
                            'delivery_crew', 'total', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        carts = Cart.objects.filter(user=user)
        total = 0
        for cart in carts:
            total += cart.price
        order_data = {
            'user': user,
            'delivery_crew': None,
            'status': 0,
            'total': total,
            'date': datetime.now(),
        }
        return Order.objects.create(**order_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'status': {'min_value': 0, 'max_value': 1}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
