from django.contrib.auth.models import User

from rest_framework import serializers
from ..track.models import Track

class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class TrackSerializer(serializers.ModelSerializer):

    # user = UserSerializer()

    class Meta:
        model = Track
        fields = ('user', 'created_at', 'location')
