from django.conf import settings
import requests
from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def verify_email(self):
        email = self.validated_data['email']

        if settings.HUNTER_API_KEY:
            params = {
                'email': email,
                'api_key': settings.HUNTER_API_KEY
            }
            url = settings.HUNTER_EMAIL_VERIFIER_URL
            response = requests.get(url, params=params).json()

            if not response['data']['result'] == 'deliverable':
                raise serializers.ValidationError('Invalid email.')

        return email

    url = serializers.HyperlinkedIdentityField(view_name='users-detail')
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['url', 'email', 'password']
