"""views for the user api"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response

from base import models
from base import serializers

from django.contrib.auth.hashers import make_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = serializers.UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = models.User.objects.create(
            email=data['email'],
            name=data['name'],
            password=make_password(data['password']),
        )
        serializer = serializers.UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'user with this email already exists.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = serializers.UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = models.User.objects.all()
    serializer = serializers.UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = models.User.objects.get(id=pk)
    serializer = serializers.UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = models.User.objects.get(id=pk)

    data = request.data

    user.name = data['name']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()

    serializer = serializers.UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    user = models.User.objects.get(id=pk)
    user.delete()
    return Response('user was deleted')
