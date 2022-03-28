from rest_framework import viewsets,mixins
from rest_framework import generics
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from django.db.models.query import QuerySet
import requests


# ViewSets define the view behavior.

class AccountUserCreate(generics.CreateAPIView):
    queryset = AccountUser.objects.all()
    serializer_class = AccountUserSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def perform_create(self, serializer):
        qq=self.request.user
        auuser = User.objects.get(username=self.request.user)
        serializer.save(user_id = auuser.id)


class AccountUserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = AccountUser.objects.all()
    serializer_class = AccountUserSerializer
    lookup_field = 'user_id'
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        auuser = User.objects.get(username=self.request.user)
        filter_kwargs = {self.lookup_field:auuser.id}
        obj = get_object_or_404(queryset,**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        js_code = self.request.data['code']
        appid='wxde353f9aa5fd513d'
        secret='40d444aaafcdd90cb5d106ef5590c6c6'
        requestString='https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code'.format(APPID=appid,SECRET=secret,JSCODE=js_code)
        r = requests.get(requestString)
        r=r.json()
        openid=r['openid']
        #openid='baduser002'
        try:
            auth_user = User.objects.get(username=openid)
        except:
            auth_user = User.objects.create(username=openid)
        try:
            token = Token.objects.get(user=auth_user)
        except:
            token = Token.objects.create(user=auth_user)
        return Response(token.key, status=status.HTTP_201_CREATED)


class ProductAbstractList(generics.ListAPIView):
    serializer_class = ProductAbstractSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'zone'
    def get_queryset(self):
        queryset =  ProductAbstract.objects.all()
        auuser = User.objects.get(username=self.request.user)
        accountuser=AccountUser.objects.get(user_id=auuser.id)
        filter_kwargs = {self.lookup_field:accountuser.zone}
        queryset = get_list_or_404(queryset,**filter_kwargs)
        return queryset


class ProductDetailList(generics.ListAPIView):
    #queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'product_id'
    lookup_url_kwarg = 'product'
    def get_queryset(self):
        queryset = ProductDetail.objects.all()
        filter_kwargs = {self.lookup_field:self.kwargs[self.lookup_url_kwarg]}
        queryset = get_list_or_404(queryset,**filter_kwargs)
        # related_images = ImageItems.objects.filter(ProductAbstract_id=self.kwargs[self.lookup_url_kwarg])
        # list_related_images = get_list_or_404(related_images)
        # for i in list_related_images:
        #     queryset.append(i)
        #related_images=ImageItems.objects.filter(Product_id=self.kwargs[self.lookup_url_kwarg])
        #query_related_images=[(i.id,i.image_select.name) for i in related_images]
        #此处等一等，因为下面建立的循环会把数据库锁住导致删除不了
        #print([(i.image_name,i.image_select.name) for i in related_images])
        lst1 = [(i.id,i.selectType) for i in queryset]
        for i in range(len(lst1)):
            if lst1[i][1]=='radio':
                retR = RadioItems.objects.filter(ProductDetail_id = lst1[i][0])
                queryset[i].prompt=[(i.name,i.value) for i in retR]
            elif lst1[i][1]=='picker':
                retP = PickerItems.objects.filter(ProductDetail_id = lst1[i][0])
                queryset[i].prompt =[i.value for i in retP]
            elif lst1[i][1]=='checkbox':
                retC = CheckboxItems.objects.filter(ProductDetail_id= lst1[i][0])
                queryset[i].prompt =[(i.name,i.value) for i in retC]
            #此处不同于上面写到prompt里面的是字符串，
            # 而"ProductDetail.image" must be a "ImageItems" instance
            # elif lst1[i][1] == 'show-picture':
            #     retI = ImageItems.objects.filter(id=lst1[i][0])
            #     out_image=retI.values('image_select')[0]['image_select']
            #     queryset[i].image = out_image
        return  queryset
class ImageItemsList(generics.RetrieveAPIView):
    queryset = ImageItems.objects.all()
    serializer_class = ImageItemsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'pk'
    lookup_url_kwarg = 'headimage'
class RadioItemsList(generics.ListAPIView):
    queryset = RadioItems.objects.all()
    serializer_class = RadioItemsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
class PickerItemsList(generics.ListAPIView):
    queryset = PickerItems.objects.all()
    serializer_class = PickerItemsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
class CheckboxItemsList(generics.ListAPIView):
    queryset = CheckboxItems.objects.all()
    serializer_class = CheckboxItemsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
class advertisingInfoList(generics.ListAPIView):
    queryset = advertisingInfo.objects.all()
    serializer_class = advertisingInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'product_id'
    def get_queryset(self):
        queryset = self.queryset.filter(advertiser=self.kwargs['product_id'])
        return queryset
class OrderCreate(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg='product_id'
    def create(self, request, *args, **kwargs):
        request.data['product']=self.kwargs['product_id']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        auuser = User.objects.get(username=self.request.user)
        serializer.save(SubmitUser_id = auuser.id,product_id=self.kwargs['product_id'])

class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self):
        auuser = User.objects.get(username=self.request.user)
        quer = self.queryset.filter(SubmitUser_id=auuser.id).order_by('-create_time')
        queryset = get_list_or_404(quer)[:10]
        return queryset

class ZoneSelectList(generics.ListAPIView):
    queryset = ZoneSelect.objects.all()
    serializer_class = ZoneSelectSerializer

class OrderImageList(generics.CreateAPIView):
    queryset = OrderImage.objects.all()
    serializer_class = OrderImageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


