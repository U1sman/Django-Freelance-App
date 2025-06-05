from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.db import DatabaseError
# Create your views here.


@api_view(['POST'])
def signup(request):
    data = request.data #no need to use data = json.loads(request.body) cuz of drf
    username= data['username']
    email= data['email']
    password= data['password']
    first_name= data['firstname']
    last_name= data['lastname']

    if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
        new_user = User.objects.create_user(
            username= username,
            email= email,
            password= password,
            first_name= first_name,
            last_name= last_name
        )
        
        django_login(request._request, new_user)

        return Response({
            "message": "successfully created user",
            "user_info": {
                "id": new_user.id,
                "username": username,
                "is_seller": new_user.is_seller,
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    data = request.data
    emailUsername= data['emailUsername']
    password= data['password']

    if not emailUsername or not password:
        return Response({'error': 'Email/Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=emailUsername).exists():
        login_user = User.objects.get(username= emailUsername)
    
    elif User.objects.filter(email=emailUsername).exists():
        login_user = User.objects.get(email= emailUsername)
    
    else:
        return Response({'error': 'Wrong Email or Username and/or password'}, status=status.HTTP_400_BAD_REQUEST)
    
    login_user = authenticate(request._request, username=login_user.username, password=password)
    if login_user is not None:
        django_login(request._request, login_user)

        return Response({
            "message": "successfully logged in",
            "user_info": {
                "id": login_user.id,
                "username": login_user.username,
                "is_seller": login_user.is_seller,
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Wrong Email or Username and/or password'}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        serialized_data = UserSerializer(user).data
        return Response(serialized_data)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])   
def get_all_gigs(request):
    try:
        gigs = Gig.objects.all().order_by("-created_on")
        serialized_gigs = GigSerializer(gigs, many=True).data
        return Response(serialized_gigs)
    except DatabaseError:
        return Response({"error": "Could not get all Gigs"}, status=status.HTTP_404_NOT_FOUND)
     

@api_view(['GET'])
def check_authenticated_status(request):
    if request.user.is_authenticated:
        return Response({'isAuthenticated': True})
    else:
        return Response({'isAuthenticated': False})
    

@api_view(['GET'])
def get_all_categories(request):
    try:
        categories = Category.objects.all()
        serialized_categories = CategorySerializer(categories, many=True).data
        return Response(serialized_categories)
    except DatabaseError:
        return Response({"error": "Could not get all Categories"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_categoryGigs(request, category_name):
    try:
        category = Category.objects.get(name= category_name)
        categoryGigs = Gig.objects.filter(category= category)
        serialized_gigs = GigSerializer(categoryGigs, many=True).data
        return Response(serialized_gigs)
    except Category.DoesNotExist:
        return Response({"error": "Could not get Gigs"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_gig(request, gig_id):
    try:
        gig = Gig.objects.get(pk= gig_id)
        serialized_gig = GigSerializer(gig).data
        return Response(serialized_gig)
    except Gig.DoesNotExist:
        return Response({"error": "Could not get Gig"}, status=status.HTTP_404_NOT_FOUND)
    

