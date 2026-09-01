from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Profile

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=30)
    def validate_username(self, value):
        if User.objects.filter(username=value).exists(): raise serializers.ValidationError('Ce compte existe déjà.')
        return value
    @transaction.atomic
    def create(self, data):
        user=User.objects.create_user(username=data['username'], password=data['password'], first_name=data['first_name'], last_name=data['last_name'])
        Profile.objects.create(user=user, phone=data['phone'])
        return user

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    s=RegisterSerializer(data=request.data); s.is_valid(raise_exception=True); user=s.save(); token,_=Token.objects.get_or_create(user=user)
    return Response({'token':token.key,'user':{'id':user.id,'username':user.username,'role':'CLIENT'}}, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user=authenticate(username=request.data.get('username'), password=request.data.get('password'))
    if not user: return Response({'detail':'Identifiants invalides.'}, status=400)
    token,_=Token.objects.get_or_create(user=user); profile,_=Profile.objects.get_or_create(user=user)
    return Response({'token':token.key,'user':{'id':user.id,'username':user.username,'role':profile.role,'verified':profile.verified}})
