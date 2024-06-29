from rest_framework import serializers
from .models import Event, User, Group, Registration, Category, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['bio', 'instagram_url', 'facebook_url', 'twitter_url', 'linkedin_url', 'user']

class EventSerializer(serializers.ModelSerializer):
    host = UserSerializer()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'category', 'host', 'group', 'image']

class GroupSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    members = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'privacy_setting', 'image_url', 'owner', 'members']

class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    event = EventSerializer()

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'email', 'contact_number']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
