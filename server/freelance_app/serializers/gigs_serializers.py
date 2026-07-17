from .common import * 
from freelance_app.serializers import UserSerializer, MinimalUserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DetailedGigSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    related_seller = UserSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    orders_num = serializers.IntegerField(read_only=True)
     
    class Meta:
        model = Gig
        fields = '__all__'


class MinimalGigSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source= 'related_seller.username', read_only= True)
    seller_profilepic = serializers.ImageField(source= 'related_seller.profile_pic', read_only= True)
    rating = serializers.FloatField(read_only=True)
    orders_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Gig
        fields = [
            'id',
            'title',
            'thumbnail',
            'starting_price',
            'rating',
            'orders_num',
            'seller_username',
            'seller_profilepic',
        ]


class PricingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingOption
        fields = '__all__'


class PricingOptionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingOption
        fields = [
            'id',
            'description',
        ]


class GigReviewSerializer(serializers.ModelSerializer):
    author = MinimalUserSerializer(read_only=True)
    class Meta:
        model = GigReview
        fields = '__all__'


#CREATE 
class CreatePricingOptionSerializer(serializers.ModelSerializer):
    #Coverts the tier string from the frontend into a django textchoice as defined in the models
    tier = serializers.ChoiceField(choices=PricingOption.Tier.choices)
    class Meta:
        model = PricingOption
        fields = [
            'tier',
            'price',
            'delivery_days',
            'description',
        ]


class CreateGigAndPricingOptionSerializer(serializers.ModelSerializer):
    pricing_options = CreatePricingOptionSerializer(many=True)
    thumbnail = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Gig        
        fields = [
            'title',
            'description',
            'category', 
            'thumbnail', 
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
        # Loop, instantiate, and bulk create the options(bulk create batches all the options together and creates them in one query only)
        options_to_create = [
            PricingOption(
                related_gig=gig, 
                tier=option_data['tier'],
                price=option_data['price'],
                delivery_days=option_data['delivery_days'],
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