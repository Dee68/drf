from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User, Profile
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password1']

        extra_kwargs = {
            'password': {'write_only': True},
            'password1': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data['username']
        passw = validated_data['password']
        passw1 = validated_data['password1']
        if not username.isalnum():
            raise serializers.ValidationError({'error': 'Username should only be alpha numeric characters.'})
        if passw != passw1:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class EmailvericationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=60, min_length=3)
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)
    username = serializers.CharField(max_length=20, min_length=2, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        # filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)
        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email not verified, verify email and try again')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    class Meta:
        model = User
        fields = ['refresh']
    
    default_error_messages = {
        'bad_token': 'Invalid token or token have expired'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
        
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError(self.default_error_message)
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'
        