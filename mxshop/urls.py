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
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

# from goods.views_base import GoodsListView
from goods.views import GoodsListView, CategoryViewset
from mxshop.settings import MEDIA_ROOT

from user.views import SmsCodeViewset, UserViewset


# 只使用viewsets完成商品列表的url配置
# goods_list = GoodsListView.as_view({
#     'get': 'list',  # 将get请求绑定到list
# })

# 使用viewsets和router完成商品列表页
router = DefaultRouter()

# 把goods注册到router中, base_name给url命名，不然就按照模型里面默认定义
router.register(r'goods', GoodsListView, base_name="goods")

# 配置Category的url
router.register(r'categories', CategoryViewset, base_name="categories")

# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code"),

# 配置users的url
router.register(r'users', UserViewset, base_name="users")

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor', include('DjangoUeditor.urls')),

    # drf自带的token授权登录,获取token需要向该地址post数据
    path('api-token-auth/', views.obtain_auth_token),

    # jwt的token认证，前面的url路径可随意写
    path('jwt-auth/', obtain_jwt_token),

    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    # 商品列表页
    # path('goods/', GoodsListView.as_view(), name="goods-list"),
    # path('goods/', goods_list, name="goods-list"),

    # router的path路径
    re_path('^', include(router.urls)),
    # 生成drf自动化文档
    path('docs/', include_docs_urls(title='超市文档')),
    # 给rest_framework配置网页登录的url
    path('api-auth/', include('rest_framework.urls')),
]
