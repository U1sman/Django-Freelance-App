from rest_framework import serializers
from django_countries.serializer_fields import CountryField as CountrySerializerField
from .models import *

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()
    class Meta:
        model= User
        fields = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'profile_pic',
        'country',
        'languages',
        'skills',
        'is_seller',
        'joined_date',
    ]
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Education
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model= Skill
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model= Language
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = '__all__'


class GigReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= GigReview
        fields = '__all__'


class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= SellerReview
        fields = '__all__'

    
class GigSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model= Gig
        fields = '__all__'