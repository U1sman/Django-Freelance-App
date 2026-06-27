from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.db import DatabaseError

@api_view(['GET'])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id= order_id)
        serialized_order = OrderSerializer(order).data
        return Response(serialized_order)
    except Order.DoesNotExist:
        return Response({"error": "Could not get Order"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_order_deliveries(request, order_id):
    try:
        order = Order.objects.get(id= order_id)
        deliveries = order.deliveries.all().order_by("-created_at")
        serialized_deliveries = DeliverySerializer(deliveries, many=True).data
        return Response(serialized_deliveries)
    
    except Order.DoesNotExist:
        return Response({"error": "Could not get Order"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def create_order(request):
    try:
        data = request.data
        gig = Gig.objects.get(id=data["gig"]["id"])
        pricing_option = PricingOption.objects.get(id=data["pricingOption"]["id"])
        requirements = data.get("requirements", "").strip()

        if not requirements or not 3000 >= len(requirements) >= 200:
            return Response({"error": "Requirements are required."}, status=status.HTTP_400_BAD_REQUEST)
        # Check if the pricing option belongs to this gig
        if pricing_option.related_pricingPlan.related_gig != gig:
            return Response({"error": "Pricing option does not match the gig"}, status=400)

    except Gig.DoesNotExist:
        return Response({"error": "Gig does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except PricingOption.DoesNotExist:
        return Response({"error": "Pricing Option does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    

    if not Order.objects.filter(buyer=request.user, seller=gig.related_seller, related_gig=gig, status="ACTIVE").exists():
        if gig not in request.user.gigs.all():
            order = Order(buyer= request.user, seller=gig.related_seller, related_gig= gig, related_pricing_option=pricing_option, requirements=requirements)
            order.save()
            return Response({
                "message": "Order created successfully.",
                "order_id": order.id,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You cannot buy your own Gig"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Not more than 1 order a time"}, status=status.HTTP_400_BAD_REQUEST)