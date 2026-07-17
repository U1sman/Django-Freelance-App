from .common import *

@api_view(['GET'])
def get_order(request, order_id):
    try:
        user = request.user

        if user.is_seller:
            order_queryset = Order.objects.select_related('related_gig', 'related_pricing_option', 'buyer').order_by('-placed_at').get(id= order_id ,seller=user)
        else:
            order_queryset = Order.objects.select_related('related_gig', 'related_pricing_option', 'seller').order_by('-placed_at').get(id= order_id, buyer=user)

        serialized_order = MinimalOrderSerializer(order_queryset, context= {'request': request}).data
        return Response(serialized_order)
    except Order.DoesNotExist:
        return Response({"error": "Could not get Order"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Failed to get order: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_orders(request):
    try:
        user = request.user

        if user.is_seller:
            orders_queryset = Order.objects.filter(seller=user).select_related('related_gig', 'related_pricing_option', 'buyer').order_by('-placed_at')
        else:
            orders_queryset = Order.objects.filter(buyer=user).select_related('related_gig', 'related_pricing_option', 'seller').order_by('-placed_at')

        order_status = request.query_params.get('order_status', None)
        if order_status:
            orders_queryset = orders_queryset.filter(status__iexact=order_status)
        
        paginator = LimitOffsetPagination()
        paginator.default_limit = 5
        # paginator.max_limit = 12
        paginator.limit_query_param = "orders_num"
        paginator.offset_query_param = "orders_start"
        paginated_orders = paginator.paginate_queryset(orders_queryset, request)

        serialized_orders = MinimalOrderSerializer(paginated_orders, many= True, context= {'request': request}).data
        return paginator.get_paginated_response(serialized_orders)
    except Order.DoesNotExist:
        return Response({"error": "No orders to display"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": f"Failed to get orders: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_order_deliveries(request, order_id):
    try:
        order = get_object_or_404(
                    Order.objects.prefetch_related('deliveries__attachments', 'deliveries__sender'), 
                    id=order_id
                )
        
        if request.user.id != order.buyer_id and request.user.id != order.seller_id:
            return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
        
        deliveries = order.deliveries.all()
        serialized_deliveries = DeliverySerializer(deliveries, many=True).data 
        return Response(serialized_deliveries, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Failed to get deliveries: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_requirements(request, order_id):
    try:
        order_data = Order.objects.filter(id=order_id).values('buyer_id', 'seller_id', 'requirements', 'reqs_submitted_at').first()

        if not order_data:
            return Response({"detail": "Order Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id != order_data['buyer_id'] and request.user.id != order_data['seller_id']:
            return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)
        return Response({"requirements": order_data['requirements'],
                         "reqs_submitted_at": order_data['reqs_submitted_at']}, status= status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"Failed to get requirements: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_activities(request, order_id):
    try:
        order_data = get_object_or_404(Order.objects.values('buyer_id', 'seller_id'), id=order_id)
        
        if request.user.id != order_data['buyer_id'] and request.user.id != order_data['seller_id']:
            return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

        order_activities = OrderActivity.objects.filter(related_order_id = order_id)
        if not order_activities.exists():
            return Response({"detail": "No order activities found for this gig."}, status=status.HTTP_404_NOT_FOUND)
        serialized_order_activities = OrderActivitySerializer(order_activities, many=True).data
        return Response(serialized_order_activities, status= status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"Failed to get order activities: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pricing_option_details(request, order_id):
    try:
        order_data = get_object_or_404(Order.objects.values('buyer_id', 'seller_id', 'related_pricing_option_id'), id=order_id)
        
        if request.user.id != order_data['buyer_id'] and request.user.id != order_data['seller_id']:
            return Response({"detail": "Unauthorized."}, status=status.HTTP_403_FORBIDDEN)

        pricing_option = PricingOption.objects.filter(id=order_data['related_pricing_option_id']).first()
        if not pricing_option:
            return Response({"detail": "No pricing options found for this gig."}, status=status.HTTP_404_NOT_FOUND)
        serialized_pricing_option = PricingOptionDetailsSerializer(pricing_option).data
        return Response(serialized_pricing_option, status= status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": f"Failed to get pricing option : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# put this logic into the serializer instead of the api later
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        data = request.data
        gig = Gig.objects.get(id=data["gig"]["id"])
        pricing_option = PricingOption.objects.get(id=data["pricingOption"]["id"])
        requirements = data.get("requirements", "").strip()

        if not requirements or not 3000 >= len(requirements) >= 200:
            return Response({"error": "Requirements are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        if pricing_option.related_gig != gig:
            return Response({"error": "Pricing option does not match the gig"}, status=status.HTTP_400_BAD_REQUEST)

        if not Order.objects.filter(buyer=request.user, seller=gig.related_seller, related_gig=gig, status="ACTIVE").exists():
            if gig not in request.user.gigs.all():
                order = Order(
                    buyer=request.user, 
                    seller=gig.related_seller, 
                    related_gig=gig, 
                    related_pricing_option=pricing_option, 
                    requirements=requirements
                )
                order.save()
                return Response({
                    "message": "Order created successfully.",
                    "order_id": order.id,
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "You cannot buy your own Gig"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Not more than 1 order a time"}, status=status.HTTP_400_BAD_REQUEST)

    except Gig.DoesNotExist:
        return Response({"error": "Gig does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except PricingOption.DoesNotExist:
        return Response({"error": "Pricing Option does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Failed to create order: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_activity(request):
    try:
        serializer = CreateOrderActivitySerializer(data= request.data, context= {'request': request})
        if serializer.is_valid():
            new_activity = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Order Activity created successfully",
                    "activity_id": str(new_activity.id)
                },
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": f"Failed to create order activity: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_delivery(request):
    try:
        serializer = CreateDeliverySerializer(data= request.data, context= {'request': request})
        if serializer.is_valid():
            new_delivery = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Order Delivery created successfully",
                    "activity_id": str(new_delivery.id)
                },
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": f"Failed to create order delivery: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_revision_request(request):
    try:
            serializer = CreateRevisionRequestSerializer(data= request.data, context= {'request': request})
            if serializer.is_valid():
                new_revision = serializer.save()
                return Response(
                    {
                        "status": "success",
                        "message": "Order revision created successfully",
                        "activity_id": str(new_revision.id)
                    },
                    status= status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
            return Response({"error": f"Failed to create order revision: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     