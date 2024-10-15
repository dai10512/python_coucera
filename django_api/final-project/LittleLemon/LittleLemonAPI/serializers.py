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
    user = UserSerializer(read_only=True)
    quantity = serializers.IntegerField(write_only=True)
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'quantity', 'menuitem', 'price', 'unit_price']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        # 必要なフィールドを計算して設定
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

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    foreign_key = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
