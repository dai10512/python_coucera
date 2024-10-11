from rest_framework import serializers
from .models import Category, MenuItem


class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'title']


class MenuItemSerializer (serializers.ModelSerializer):
    # 外部キーとしてのCategoryの入力値
    category_id = serializers.IntegerField(write_only=True)
    # 外部キーとしてのCAtegoryの出力値
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price',
                  'inventory', 'category', 'category_id']
