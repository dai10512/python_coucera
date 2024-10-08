
from rest_framework import serializers
from .models import Rating
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User


class RatingSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # モデル
        model = Rating

        # 表示及び受け付けるフィールド
        fields = ['user', 'menuitem_id', 'rating']

        # 重複チェック
        validators = [UniqueTogetherValidator(
            queryset=Rating.objects.all(),
            fields=['user', 'menuitem_id', 'rating'],
        )]

        # 入力値の制限
        extra_kwargs = {
            'rating': {
                'min_value': 0,
                'max_value': 5,
            }
        }
