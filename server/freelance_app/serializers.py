from rest_framework import serializers
from django_countries.serializer_fields import CountryField as CountrySerializerField
from .models import *
from datetime import datetime, timedelta

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializerField()
    country_name = serializers.SerializerMethodField()
    class Meta:
        model = User
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
            'date_joined',
        ]
        
    def get_country_name(self, obj):
        return obj.country.name if obj.country else None


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_pic', 'first_name', 'last_name', 'date_joined']


class OrderSerializer(serializers.ModelSerializer):
    delivery_date = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_delivery_date(self, obj):
        return obj.placed_at + timedelta(days=obj.related_pricing_option.delivery_time)
   

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GigReviewSerializer(serializers.ModelSerializer):
    author = MinimalUserSerializer(read_only=True)
    class Meta:
        model = GigReview
        fields = '__all__'


class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = '__all__'


class PricingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingOption
        fields = '__all__'


class PricingPlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PricingPlan
        fields = '__all__'


class DetailedGigSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    pricing_plan = PricingPlanSerializer(read_only=True)
    related_seller = UserSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    orders_num = serializers.IntegerField(read_only=True)
     
    class Meta:
        model = Gig
        fields = '__all__'


class MinimalGigSerializer(serializers.ModelSerializer):
    related_seller = MinimalUserSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    orders_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Gig
        fields = [
            'id',
            'title',
            'cover_image',
            'starting_price',
            'related_seller',
            'rating',
            'orders_num',
        ] 


class DeliveryAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAttachment
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    attachments = DeliveryAttachmentSerializer(many=True, read_only=True)
    sender = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = '__all__'


class OrderActivityLog(serializers.ModelSerializer):
    class Meta:
        model = OrderActivityLog
        fields = '__all__'


class OrderActivity(serializers.ModelSerializer):
    class Meta:
        model = OrderActivity
        fields = '__all__'


class Offer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class Quotation(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'


