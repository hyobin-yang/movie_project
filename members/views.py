# from django.shortcuts import render
# from .models import CustomUser
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import LoginSerializer, SignupSerializer
# from django.contrib import auth
# from django.contrib.auth.hashers import make_password


# # Create your views here.
# @api_view(['POST'])
# def login(request):
#     serializer = LoginSerializer(data=request.data)
#     if serializer.is_valid():
#         user = auth.authenticate(
#             request=request,
#             username=serializer.data['username'],
#             password=serializer.data['password']
#         )
#         if user is not None:
#             auth.login(request, user)
#             return Response(status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         new_user = serializer.save(password = make_password(serializer.validated_data['password']))
#         auth.login(request, new_user)
#         return Response(status=status.HTTP_200_OK)
#     return Response(status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def logout(request):
#     auth.logout(request)
#     return Response(status=status.HTTP_200_OK)


##
from django.shortcuts import render

from django.contrib import auth
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser
from .serializers import NicknameUniqueCheckSerializer, CustomRegisterSerializer, CustomLoginSerializer, \
    CustomValidationError




class CustomLoginView(APIView):
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except CustomValidationError as e:
            error_detail = dict(e.detail)
            return Response(error_detail, status=status.HTTP_204_NO_CONTENT)

        # 로그인 성공 시 필요한 로직 수행
        # ...
        return Response({'message': 'Login successful'}, status=200)


class NicknameUniqueCheck(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = NicknameUniqueCheckSerializer
    ## 변경
    authentication_classes = [JWTAuthentication]

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({'detail':'available nickname'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'nickname is not unique'}, status=status.HTTP_204_NO_CONTENT)
