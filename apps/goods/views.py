
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer
from .filters import GoodsFilter

# 实现商品列表页方法1
# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[10:]
#         # 参数many=True是因为goods是一个含多个元素的列表
#         goods_serializer = GoodsSerializer(goods, many=True)
#         return Response(goods_serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 商品列表页方法2
# class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# 自定义商品列表分页类，和方法3一起用
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# 商品列表页方法3
# class GoodsListView(generics.ListAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination


# 商品列表页方法4, 使用viewsets和router，需要在urls.py中设置
# class GoodsListView(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination


# drf过滤方法1
# class GoodsListView(mixins.ListModelMixin, viewsets.GenericViewSet):
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination
#
#     def get_queryset(self):
#         queryset = Goods.objects.all()
#         price_min = self.request.query_params.get("price_min", 0)
#         if price_min:
#             # 后面加上排序方式避免报错
#             queryset = queryset.filter(shop_price__gt=int(price_min)).order_by('-add_time')
#         return queryset


# drf过滤方法2， 使用DjangoFilterBackend(精确到一个字段的过滤, 必须是精确匹配值进行过滤)，以及搜索和排序
class GoodsListView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all().order_by('-add_time')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # 设置列表页的单独auth认证，因为商品列表是一个公开页，不需要认证，所以正常情况下应该把这行注释掉
    # authentication_classes = (TokenAuthentication,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'shop_price')
    filter_class = GoodsFilter

    # 使用filters.SearchFilter进行搜索
    search_fields = ('name', 'goods_brief', 'goods_desc')

    # 使用filters.OrderingFilter设置排序
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)  # 第一类商品类别数据
    serializer_class = CategorySerializer

