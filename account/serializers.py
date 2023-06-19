from rest_framework import serializers
from account.models import User, Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password1']

        extra_kwargs = {
            'password': {'write_only': True},
            'password1': {'write_only': True}
        }

    def create(self, validate_data):
        username = validate_data['username']
        passw = validate_data['password']
        passw1 = validate_data['password1']
        if not username.isalnum():
            raise serializers.ValidationError({'error': 'Username should only be alpha numeric characters.'})
        if passw != passw1:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance