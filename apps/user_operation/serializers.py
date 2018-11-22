__author__ = 'Administrator'

from rest_framework import serializers
from .models import UserFav
from rest_framework.validators import UniqueTogetherValidator


# 商品详情页实现用户收藏接口
class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        # 使用validate方式实现唯一联合,这里也就是user, goods联合字段数据重复时的处理
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

        fields = ("user", "goods", "id")