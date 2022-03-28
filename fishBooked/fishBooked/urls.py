"""fishBooked URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import include
from rest_framework import routers
from fish.views import *
from fish import wviews
from rest_framework.authtoken import views

# Routers provide an easy way of automatically determining the URL conf.



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^account-user-Create', AccountUserCreate.as_view()),
    url(r'^account-user-RetrieveUpdate',AccountUserRetrieveUpdate.as_view()),
    url(r'^token', UserCreate.as_view()),
    url(r'^product-abstract', ProductAbstractList.as_view()),
    url(r'^product/(?P<product>[0-9]+)/detail', ProductDetailList.as_view()),
    url(r'^product-headimage/(?P<headimage>[0-9]+)', ImageItemsList.as_view()),
    url(r'^order/(?P<product_id>[0-9]+)', OrderCreate.as_view()),
    url(r'^order-list/', OrderList.as_view()),
    url(r'^order-images/', OrderImageList.as_view()),
    url(r'^advertisingInfoList/(?P<product_id>[0-9]+)', advertisingInfoList.as_view()),
    url(r'^zones', ZoneSelectList.as_view()),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^image', wviews.index)
]

#username:wt
#password:passwordWT99
#zhishifenzi
#qinglaoderenF8
#无聊人士
#wuliaorenSHI
#1	pbkdf2_sha256$36000$LO4Ups2R1hHs$69bLiZmOnpxvg2IrMzEUzC6q80vrWv3lWHJlCl/uPcU=	2017-10-09 11:30:04.903651	1			2718339969@qq.com	1	1	2017-10-08 03:44:18.057763	wt
