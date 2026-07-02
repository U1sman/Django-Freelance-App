from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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
from django.db.models import Avg, Count, Q
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

@api_view(['GET'])   
def get_gigs(request):
    try:
        gigs_queryset = Gig.objects.select_related('related_seller').annotate(
            rating=Avg('gig_reviews__rating'),
            orders_num=Count('gig_orders', filter=Q(gig_orders__status="COMPLETED"), distinct=True)
        ).order_by('-created_on')

        search_title = request.query_params.get('search', None)
        category_name = request.query_params.get('category', None)
        seller_id = request.query_params.get('seller_id', None)
        if search_title:
            gigs_queryset = gigs_queryset.filter(title__icontains=search_title)
        if category_name:
            gigs_queryset = gigs_queryset.filter(category__name__iexact=category_name)
        if seller_id:
            gigs_queryset = gigs_queryset.filter(related_seller_id=seller_id)

        paginator = LimitOffsetPagination()
        paginator.default_limit = 12
        paginator.max_limit = 12
        paginator.limit_query_param = "gigs_num"
        paginator.offset_query_param = "gigs_start"
        paginated_gigs = paginator.paginate_queryset(gigs_queryset, request)

        serialized_gigs = MinimalGigSerializer(paginated_gigs, many=True).data
        return paginator.get_paginated_response(serialized_gigs)
    except Exception as e:
        return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_gig(request, gig_id):
    try:
        gig = Gig.objects.filter(id= gig_id).select_related(
            'related_seller', 
            'category', 
            'pricing_plan'
        ).prefetch_related(
            'related_seller__languages', 
            'related_seller__skills',
            'pricing_plan__pricing_options'
        ).annotate(
            rating=Avg('gig_reviews__rating'),
            orders_num=Count('gig_orders', filter=Q(gig_orders__status="COMPLETED"), distinct=True)
        ).first()
        serialized_gig = DetailedGigSerializer(gig).data
        return Response(serialized_gig)
    except Gig.DoesNotExist:
        return Response({"error": "Could not get Gig"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Failed to get gigr: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_all_categories(request):
    try:
        categories = Category.objects.all()
        serialized_categories = CategorySerializer(categories, many=True).data
        return Response(serialized_categories)
    except Exception as e:
        return Response({"error": f"Failed to get all categories {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_gig_reviews(request, gig_id):
    try:
        gig_reviews = GigReview.objects.filter(related_gig= gig_id).select_related("author").order_by("-created_at")
        paginator = LimitOffsetPagination() 
        paginator.default_limit = 5
        paginator.max_limit = 5
        paginator.limit_query_param = "reviews_num"
        paginator.offset_query_param = "reviews_start"
        paginated_gig_reviews = paginator.paginate_queryset(gig_reviews, request)
        serialized_gig_reviews = GigReviewSerializer(paginated_gig_reviews, many=True).data
        return paginator.get_paginated_response(serialized_gig_reviews)
    except GigReview.DoesNotExist:
        return Response({"error": f"No reviews found for the gig: {gig_id}"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Failed to get reviews: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_gig_review(request):
    try:
        serializer = CreateGigReviewSerializer(data= request.data, context= {'request': request})
        if serializer.is_valid():
            new_review = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Gig review created successfully",
                    "review_id": str(new_review.id)
                },
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": f"Failed to create gig review: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_gig_and_pricing_plan(request):
    try:
        serializer = CreateGigAndPricingPlanSerializer(data= request.data, context= {'request': request})
        if serializer.is_valid():
            new_gig = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Gig, PricingPlan and PricingOptions Created Successfully ",
                    "gig_id": str(new_gig.id)
                },
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Failed to create gig: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
