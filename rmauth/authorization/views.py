from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Profile, Requisites
from .serializers import (
    RegistrationSerializer, LoginSerializer, CustomUserSerializer, ProfileSerializer, RequisitesSerializer
)
from .renderers import CustomUserJSONRenderer
from .token_generators import generate_rt, generate_jwt


# Create your views here.


class RefreshView(APIView):
    """
    Refreshing old access token
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='access_token for get refresh_token'),
        }
    ))
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            user = CustomUser.objects.get(refresh_token=refresh_token)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'User does not exist'
            }, status=status.HTTP_418_IM_A_TEAPOT)
        user.refresh_token = generate_rt()
        user.save(update_fields=('refresh_token',))
        data = {
                'access_token': generate_jwt(user.pk),
                'refresh_token': user.refresh_token
        }
        return Response(data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (CustomUserJSONRenderer,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email - using like username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='user password')
        }
    ))
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (CustomUserJSONRenderer,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email - using like username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='user password')
        }
    ))
    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomUserJSONRenderer,)
    serializer_class = CustomUserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email - using like username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='user password')
        }
    ))
    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'avatar': openapi.Schema(type=openapi.TYPE_STRING, description='avatar - user avatar'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='name - user or organization name'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description="user's mobile phone"),
        }
    ))
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        data = request.data
        if data['avatar']:
            profile.avatar = data['avatar']
        if data['name']:
            profile.fio = data['name']
        if data['phone']:
            profile.phone = data['phone']
        profile.save()
        return Response(status=status.HTTP_200_OK)


class ProfileIDAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer

    def get(self, request, user_id):
        profile = Profile.objects.get(user=CustomUser.objects.get(pk=user_id))
        serializer = self.serializer_class(data=profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='user email'),
            'avatar': openapi.Schema(type=openapi.TYPE_FILE, description='avatar - user avatar'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='name - user or organization name'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description="user's mobile phone"),
        }
    ))
    def post(self, request):
        data = request.data
        Profile.objects.get_or_create(
            user=request.user,
            avatar=data["avatar"],
            name=data["name"],
            phone=data["phone"]
        )
        return Response(status=status.HTTP_201_CREATED)


class CreateRequisitesAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RequisitesSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='user email'),
            'inn': openapi.Schema(type=openapi.TYPE_STRING, description='user INN(ИНН)'),
            'payment': openapi.Schema(type=openapi.TYPE_STRING, description='payment - user or organization payment'),
            'bank_name': openapi.Schema(type=openapi.TYPE_STRING, description='bank name, where user is in'),
            'bik': openapi.Schema(type=openapi.TYPE_STRING, description='bik'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='city'),
            'cor_payment': openapi.Schema(type=openapi.TYPE_STRING, description='cor_payment'),
        }
    ))
    def post(self, request):
        data = request.data
        Requisites.objects.get_or_create(
            user=request.user,
            inn=data['inn'],
            payment=data['payment'],
            bank_name=data['bank_name'],
            bik=data['bik'],
            city=data['city'],
            cor_payment=data['cor_payment']
        )
        return Response(status=status.HTTP_201_CREATED)


class RequisitesAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RequisitesSerializer

    def get(self, request):
        profile = Requisites.objects.get(user=request.user)
        serializer = self.serializer_class(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'inn': openapi.Schema(type=openapi.TYPE_STRING, description='user INN(ИНН)'),
            'payment': openapi.Schema(type=openapi.TYPE_STRING, description='payment - user or organization payment'),
            'bank_name': openapi.Schema(type=openapi.TYPE_STRING, description='bank name, where user is in'),
            'bik': openapi.Schema(type=openapi.TYPE_STRING, description='bik'),
            'city': openapi.Schema(type=openapi.TYPE_STRING, description='city'),
            'cor_payment': openapi.Schema(type=openapi.TYPE_STRING, description='cor_payment'),
        }
    ))
    def post(self, request):
        requisites = Requisites.objects.get(user=request.user)
        data = request.data
        if data['inn']:
            requisites.inn = data['inn']
        if data['payment']:
            requisites.payment = data['payment']
        if data['bank_name']:
            requisites.bank_name = data['bank_name']
        if data['bik']:
            requisites.bik = data['bik']
        if data['city']:
            requisites.city = data['city']
        if data['cor_payment']:
            requisites.cor_payment = data['cor_payment']
        requisites.save()
        return Response(status=status.HTTP_200_OK)


class RequisitesIDAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RequisitesSerializer

    def get(self, request, user_id):
        if Profile.objects.get(user=request.user).role == 'Developer':
            profile = Requisites.objects.get(user=CustomUser.objects.get(pk=user_id))
            serializer = self.serializer_class(data=profile)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
