from rest_framework import serializers
from .models import  Product , WishListItems,BusinessProfile
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

 #Wishlist Serializers

class WishListItemsTestSerializer(serializers.ModelSerializer):    
    class Meta:
        model = WishListItems
        fields = ['id','item']
        depth = 2  


class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'

class EmployeeLogin2Serializer2(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLogin2
        fields = '__all__'

class AssignTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignTask
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessage
        fields = '__all__'

class UserRecentAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecentAds
        fields='__all__'        