from rest_framework import serializers
from django_countries.serializer_fields import CountryField as CountrySerializerField
from .models import *
from datetime import datetime, timedelta
import json

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


class OrderActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderActivityLog
        fields = '__all__'


class OrderActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderActivity
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'


class CreatePricingOptionSerializer(serializers.ModelSerializer):
    #Coverts the tier string from the frontend into a django textchoice as defined in the models
    tier = serializers.ChoiceField(choices=PricingOption.Tier.choices)
    class Meta:
        model = PricingOption
        fields = [
            'tier',
            'price',
            'delivery_time',
            'description',
        ]


class CreateGigAndPricingPlanSerializer(serializers.ModelSerializer):
    pricing_options = CreatePricingOptionSerializer(many=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Gig        
        fields = [
            'title',
            'description',
            'category', 
            'cover_image', 
            'starting_price', 
            'allow_custom_offers',
            'pricing_options'
        ]   
        
    def validate_pricing_options(self, value):
        # FormData sends arrays as stringified JSON strings. This is for parsing
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid JSON string format for pricing options.")

        # Must be exactly 3 pricing options
        if len(value) != 3:
            raise serializers.ValidationError("You must provide exactly 3 pricing options.")
        
        # Must have one of each Pricing Option Tier 
        submitted_tiers = [item.get('tier') for item in value]
        required_tiers = {PricingOption.Tier.BASIC, PricingOption.Tier.STANDARD, PricingOption.Tier.PREMIUM}
        
        if set(submitted_tiers) != required_tiers:
            raise serializers.ValidationError("You must provide exactly one BASIC, one STANDARD, and one PREMIUM tier.")
            
        return value  
           
    def create(self, validated_data):
        # Pop the nested options out before creating the Gig row and place them into this variable
        pricing_options_data = validated_data.pop('pricing_options')
        seller = self.context['request'].user
        gig = Gig.objects.create(related_seller=seller, **validated_data)
        pricing_plan = PricingPlan.objects.create(related_gig=gig)
        # Loop, instantiate, and bulk create the options(bulk create batches all the options together and creates them in one query only)
        options_to_create = [
            PricingOption(
                related_pricingPlan=pricing_plan, 
                tier=option_data['tier'],
                price=option_data['price'],
                delivery_time=option_data['delivery_time'],
                description=option_data.get('description', '')
            )
            for option_data in pricing_options_data
        ]
        PricingOption.objects.bulk_create(options_to_create)

        return gig


class CreateGigReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= GigReview
        fields= [
            'related_order',
            'body',
            'rating',
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        order = attrs.get('related_order')
        gig = order.related_gig

        if order.buyer != user:
            raise serializers.ValidationError("This order does not belong to you.")

        if order.status != "COMPLETED":
            raise serializers.ValidationError("You can only review completed orders.")

        if gig.related_seller == user:
            raise serializers.ValidationError("You cannot leave a review on your own gig.")
        
        # if gig.id != order.related_gig.id:
        #     raise serializers.ValidationError("Order does not belong to gig.")
        
        if GigReview.objects.filter(related_order=order).exists():
            raise serializers.ValidationError("A review already exists for this order.")
        
        attrs['author'] = user
        attrs['related_gig'] = gig

        return attrs
    
    # def create(self, validated_data):
    #     gig_review = GigReview.objects.create(**validated_data)

    #     return gig_review