#from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
from django.shortcuts import get_list_or_404

# Serializers define the API representation.
class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)

#ZoneSelect

class ZoneSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneSelect
        fields = ('name','address')

class ImageItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageItems
        fields = ('image_select',)

class AccountUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = ('name','mobile','province','city','country','detail','zone','the_index')

class ProductAbstractSerializer(serializers.ModelSerializer):
    headImage = ImageItemsSerializer(read_only=True)
    # headImage=serializers.HyperlinkedRelatedField(
    #     read_only=True,
    #     view_name='headimage'
    # )
    class Meta:
        model = ProductAbstract
        fields = '__all__'


class RadioItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioItems
        fields = "__all__"
class PickerItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickerItems
        fields = "__all__"
class CheckboxItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckboxItems
        fields = "__all__"
class ProductDetailSerializer(serializers.ModelSerializer):
    image=ImageItemsSerializer(read_only=True)
    class Meta:
         model = ProductDetail
         fields = "__all__"
         #depth = 1 #并没有解开picker这个结

#radio_items = serializers.HyperlinkedRelatedField(many=True, read_only=True)
#picker_items = serializers.HyperlinkedRelatedField(many=True, read_only=True)
#checkbox_items = serializers.HyperlinkedRelatedField(many=True, read_only=True)
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth=1

class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = "__all__"

class advertisingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertisingInfo
        fields = ('banner_images',)