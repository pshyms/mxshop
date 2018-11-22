from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from user_operation.models import UserFav
from .serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly


# 用户收藏功能，添加收藏用CreateModelMixin, 取消收藏用DestroyModelMixin，只会返回我们商品的id以及这条收藏关系记录的id
class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    # 这样写，没有权限管理功能，当前用户可删除其他用户的收藏信息
    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer

    # 添加权限管理功能,如果用户未登陆，会报401错误
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    # 将JSONWebTokenAuthentication单独配置到view中, SessionAuthentication是为了获得数据
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 获取当前用户，重载get_queryset方法
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

