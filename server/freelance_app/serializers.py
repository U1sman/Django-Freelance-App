from rest_framework import serializers
from django_countries.serializer_fields import CountryField as CountrySerializerField
from .models import *

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()
    country_name = serializers.SerializerMethodField()
    class Meta:
        model= User
        fields = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'tagline',
        'profile_pic',
        'country',
        'country_name',
        'languages',
        'skills',
        'is_seller',
        'joined_date',
    ]
        
    def get_country_name(self, obj):
        return obj.country.name if obj.country else None
        

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


class PricingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= PricingOption
        fields= '__all__'


class PricingPlanSerializer(serializers.ModelSerializer):
    pricing_options = PricingOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model= PricingPlan
        fields= '__all__'


class GigSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    pricing_plan = PricingPlanSerializer(read_only=True)
    related_seller = UserSerializer()
    
    class Meta:
        model= Gig
        fields = '__all__'


