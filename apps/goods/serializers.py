__author__ = 'Administrator'
from rest_framework import serializers

from goods.models import Goods, GoodsCategory


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_font_image = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Goods.objects.create(**validated_data)


class CategorySerializer3(serializers.ModelSerializer):
    """
    商品三级类别序列化
    """
    class Meta:
        model = GoodsCategory
        fields = "__all__"


# 第二级商品类别序列化
class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


# 第一级的商品类别序列化
class CategorySerializer(serializers.ModelSerializer):
    # sub_cat是models.py中定义的parent_category字段中的外键关联参数related_name的值
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    # 进行Serializer的嵌套使用。覆盖外键字段,引用了上面定义的CategorySerializer对象
    category = CategorySerializer()

    class Meta:
        model = Goods
        # fields = ('name', 'click_num', 'market_price', 'add_time')
        fields = "__all__"





