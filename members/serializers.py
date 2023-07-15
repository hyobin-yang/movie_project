# from rest_framework import serializers
# from .models import CustomUser

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150)
#     password = serializers.CharField(max_length=128)

# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password', 'nickname', 'university']


####
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.exceptions import APIException

from .models import CustomUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from allauth.account.adapter import get_adapter
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomValidationError(APIException):
    status_code = 200
    default_detail = 'Validation error'
    default_code = 'invalid'

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'nickname']


class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required = False)
    nickname = serializers.CharField(max_length=100)


    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'nickname': self.validated_data.get('nickname', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.username = self.cleaned_data.get('username')
        user.nickname = self.cleaned_data.get('nickname')

        try:
            self.cleaned_data['password1'] == self.cleaned_data['password2']
        except serializers.ValidationError:
            msg = 'The two password fields did not match.'
            raise CustomValidationError(msg)

        user.set_password(self.cleaned_data['password1'])

        try:
            user.save()
        except IntegrityError:
            msg = 'A user with that username already exists.'
            raise CustomValidationError(msg)

        user.save()
        adapter.save_user(request, user, self)
        return user


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise CustomValidationError(msg)
                attrs['user'] = user
                return attrs
            else:
                msg = 'Unable to log in with provided credentials.'
                raise CustomValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise CustomValidationError(msg)


# 닉네임 중복 검사
class NicknameUniqueCheckSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=True, min_length=1, max_length=30,
                                     validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ['nickname']