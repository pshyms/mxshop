# -*- coding:utf-8 _*-
from django_filters import rest_framework as filters
from goods.models import Goods
from django.utils.translation import ugettext_lazy as _


class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    # 指定字段以及字段上的行为，在shop_price上进行大于等于,小于等于的过滤
    price_min = filters.NumberFilter(field_name="shop_price", lookup_expr='gte', help_text=_('大于等于本店价格'))
    price_max = filters.NumberFilter(field_name="shop_price", lookup_expr='lte', help_text=_('小于等于本店价格'))
    # 模糊查询商品名，类型是CharFilter, icontains中加i表示不区分大小写
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot']

