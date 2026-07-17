from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers.gigs_serializers import *
from ..serializers.orders_serializers import *
from ..serializers.dealings_serializers import *
from ..serializers.users_serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.db import DatabaseError
from django.db.models import Avg, Count, Q
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404