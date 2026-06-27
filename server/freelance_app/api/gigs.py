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
from django.db.models import Avg, Count, Q

@api_view(['GET'])   
def get_all_gigs(request):
    try:
        gigs = Gig.objects.select_related('related_seller').annotate(
                rating=Avg('gig_reviews__rating'),
                orders_num=Count('gig_orders', filter=Q(gig_orders__status="COMPLETED"), distinct=True)
        ).order_by('-created_on')

        serialized_gigs = DetailedGigSerializer(gigs, many=True).data
        return Response(serialized_gigs)
    except DatabaseError:
        return Response({"error": "Could not get all Gigs"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_categoryGigs(request, category_name):
    try:
        category = Category.objects.get(name= category_name)
        categoryGigs = Gig.objects.filter(category= category)
        serialized_gigs = DetailedGigSerializer(categoryGigs, many=True).data
        return Response(serialized_gigs)
    except Category.DoesNotExist:
        return Response({"error": "Could not get Gigs"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_gig(request, gig_id):
    try:
        gig = Gig.objects.get(id= gig_id)
        serialized_gig = DetailedGigSerializer(gig).data
        return Response(serialized_gig)
    except Gig.DoesNotExist:
        return Response({"error": "Could not get Gig"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_all_categories(request):
    try:
        categories = Category.objects.all()
        serialized_categories = CategorySerializer(categories, many=True).data
        return Response(serialized_categories)
    except DatabaseError:
        return Response({"error": "Could not get all Categories"}, status=status.HTTP_404_NOT_FOUND)