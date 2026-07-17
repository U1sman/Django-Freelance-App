from .common import *
from freelance_app.serializers import MinimalGigSerializer, PricingOptionSerializer, MinimalUserSerializer

class OrderSerializer(serializers.ModelSerializer):
    related_gig = MinimalGigSerializer(read_only=True)
    related_pricing_option = PricingOptionSerializer(read_only=True)
    buyer = MinimalUserSerializer(read_only=True)
    seller = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'seller', 'related_gig', 'related_pricing_option', 'status', 'price',
            'delivery_days', 'placed_at', 'due_at',    
        ]
   

class MinimalOrderSerializer(serializers.ModelSerializer):
    gig_title = serializers.CharField(source='related_gig.title', read_only=True)
    gig_thumbnail = serializers.ImageField(source='related_gig.thumbnail', read_only=True)
    counterparty_name = serializers.SerializerMethodField()
    counterparty_profile_pic = serializers.SerializerMethodField()
    pricing_option_tier = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'price', 'status', 'placed_at', 'due_at', 'pricing_option_tier',
            'gig_title', 'gig_thumbnail', 'counterparty_name', 'counterparty_profile_pic', 
            'delivery_days'
        ]

    def get_counterparty_name(self, obj):
        request = self.context.get('request')
        if request and request.user.is_seller:
            return obj.buyer.username
        else:
            return obj.seller.username

    def get_counterparty_profile_pic(self, obj):
        request = self.context.get('request')
        if request and request.user.is_seller:
            user = obj.buyer   
        else:
            user = obj.seller  

        if user.profile_pic:
            if request:
                return request.build_absolute_uri(user.profile_pic.url)
            return user.profile_pic.url
        return None

    def get_pricing_option_tier(self, obj):
        return obj.related_pricing_option.tier if obj.related_pricing_option else "CUSTOM"


class OrderActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderActivity
        fields = [
            'details',
            'created_at',
        ]


class DeliveryAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAttachment
        fields = [
            'file_url',
            'file_size',
            'file_type'
        ]


class RevisionRequestSerializer(serializers.ModelSerializer):
    buyer_username = serializers.CharField(source= 'buyer.username', read_only= True)
    buyer_profilepic = serializers.ImageField(source= 'buyer.profile_pic', read_only= True)

    class Meta:
        model = RevisionRequest
        fields = [
            'requirements',
            'created_at',
            'buyer_username',
            'buyer_profilepic',
        ]


class DeliverySerializer(serializers.ModelSerializer):
    revision_request = serializers.SerializerMethodField()
    attachments = DeliveryAttachmentSerializer(many=True, read_only=True)
    sender = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'message',
            'sender',
            'status',
            'delivered_at',
            'attachments',
            'revision_request',
        ]

    def get_revision_request(self, obj):
        # Check if this delivery record has a linked revision request
        if hasattr(obj, 'revision_request'):
            return RevisionRequestSerializer(obj.revision_request).data
        return None


#CREATE
class CreateOrderActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderActivity
        fields = [
            'related_order',
            'details',
        ]

    def validate(self, attrs):
        related_order = attrs['related_order']
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Authentication credentials were not provided.")
        user = request.user
        if user.id != related_order.buyer_id and user.id != related_order.seller_id:
            raise serializers.ValidationError(
                {"related_order": "You are not authorized to add an activity to this order."}
            )
        return attrs
    

class CreateDeliveryAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAttachment
        fields = [
            'file_url',
        ]


class CreateDeliverySerializer(serializers.ModelSerializer):
    attachments = CreateDeliveryAttachmentSerializer(many=True)
    class Meta:
        model = Delivery
        fields = [
            'related_order',
            'message',
            'attachments',
        ]

#vaidations: sender be seller of related_order, related_order exist, total delivery limits, delivery attachment limits, no more than 1 delivery at a time(check if PENDING delivery exists for the order)
    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Authentication credentials were not provided.")
        user = request.user 

        related_order = attrs['related_order']
        attachments = attrs['attachments']
        
        if user.id != related_order.seller_id:
            raise serializers.ValidationError(
                {"related_order": "You are not authorized to add a delivery to this order."}
            )
        
        if len(attachments) < 1:
            raise serializers.ValidationError(
                {"attachments": "Atleast 1 attachment file has to be uploaded."}
        )

        if len(attachments) > 5:
            raise serializers.ValidationError(
                {"attachments": "You can only upload a maximum of 5 attachment files per delivery."}
            )
            
        if related_order.deliveries.filter(status='PENDING').exists():
            raise serializers.ValidationError(
                {"detail": "A delivery is already pending review. Wait for the buyer's response."}
            )

        if related_order.deliveries.count() >= 50:
            raise serializers.ValidationError(
                {"detail": "Maximum revision limits reached for this order."}
            )
    
        return attrs
    
    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments')
        delivery_sender = self.context['request'].user

        delivery = Delivery.objects.create(sender=delivery_sender, **validated_data)

        attachments_to_create = [
            DeliveryAttachment(
                related_delivery=delivery, 
                file_url = attachment_data['file_url']
            )
            for attachment_data in attachments_data
        ]
        DeliveryAttachment.objects.bulk_create(attachments_to_create)

        return delivery
  
   
class CreateRevisionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevisionRequest
        fields = [
            'related_order',
            'related_delivery',
            'requirements'
        ]

#validations: request.user is buyer, no revsion requests for the current delivery already exist, no revision request for ACCEPTED delivery and already REJECTED delivery, related_delivery begins to related_order
#side: set the delivery to REJECTED once the revision request is made 
    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("Authentication credentials were not provided.")
        user = request.user 

        order = attrs['related_order']
        delivery = attrs['related_delivery']

        if user.id != order.buyer_id:
            raise serializers.ValidationError(
                {"order": "You are not authorized to request a revision for this delivery."}
        )

        if hasattr(delivery, 'revision_request'):
            raise serializers.ValidationError(
                {"order": "A revision has already been requested for this delivery."}
            )
        
        if delivery.status == Delivery.Status.ACCEPTED:
            raise serializers.ValidationError(
                {"order": "Revision can not be requested for already ACCEPTED delivery."}
            )
        
        if delivery.status == Delivery.Status.REJECTED:
            raise serializers.ValidationError(
                {"order": "Revision can not be requested for already REJECTED delivery."}
            )
        
        if delivery.related_order_id != order.id:
            raise serializers.ValidationError({
                "related_delivery": "This delivery does not belong to the specified order."
            })
        
        return attrs
    
    def create(self, validated_data):
        buyer = self.context['request'].user
        delivery = validated_data['related_delivery']
        RevisionRequest.objects.create(buyer=buyer, **validated_data)
        delivery.status = 'REJECTED'
        delivery.save(update_fields=['status']) 

        return validated_data

    
        
