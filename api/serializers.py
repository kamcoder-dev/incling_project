from rest_framework import serializers
from django.contrib.auth import authenticate

from incling.models import *

# Serializer for creating an profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')


# User Serializers
class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        profile.first_name = profile_data.get(
            'first_name', profile.first_name)

        profile.last_name = profile_data.get('last_name', profile.last_name)

        profile.save()

        return instance


class TaskSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Task
        fields = ('id', 'title',
                  'order_field', 'description', 'type', 'profile', 'tile')


class TileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tile
        fields = ('tile_name', 'launch_date', 'status')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only:True'}}

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data['email'], validated_data['username'], validated_data['password'])

            return user

# Login API


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Wrong Login Details")
