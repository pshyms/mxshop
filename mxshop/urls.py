"""mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

# from goods.views_base import GoodsListView
from goods.views import GoodsListView
from mxshop.settings import MEDIA_ROOT

# 使用viewsets完成商品列表的url配置
# goods_list = GoodsListView.as_view({
#     'get': 'list',  # 将get请求绑定到list
# })

# 使用viewsets和router完成商品列表页
router = DefaultRouter()
# 把goods注册到router中
router.register(r'goods', GoodsListView, base_name="goods")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor', include('DjangoUeditor.urls')),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 商品列表页
    # path('goods/', GoodsListView.as_view(), name="goods-list"),
    # path('goods/', goods_list, name="goods-list"),

    # router的path路径
    re_path('^', include(router.urls)),
    # 生成drf自动化文档
    path('docs/', include_docs_urls(title='超市文档')),
    # 配置登录的url
    path('api-auth/', include('rest_framework.urls')),
]
