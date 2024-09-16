from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from tasks.models import Manage

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password since it's not a model field
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        representation.pop('confirm_password', None)
        return representation

class ManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manage
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at']
