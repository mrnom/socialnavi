from django.conf import settings
import requests
from rest_framework import serializers

from accounts.models import User


def hunter_email_verifier(email):
    params = {
        'email': email,
        'api_key': settings.HUNTER_API_KEY
    }
    url = settings.HUNTER_EMAIL_VERIFIER_URL

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {}


def clearbit_enrichment(email):
    params = {'email': email}
    headers = {'Authorization': 'Bearer {}'.format(settings.CLEARBIT_API_KEY)}
    url = settings.CLEARBIT_ENRICHMENT_URL

    response = requests.get(url, params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users-detail')
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'url',
            'email',
            'password',
            'first_name',
            'last_name',
            'location',
            'bio',
            'site',
            'avatar',
        ]

    def verify_email(self):
        email = self.validated_data['email']

        if settings.HUNTER_API_KEY:
            response = hunter_email_verifier(email)

            if not response['data']['result'] == 'deliverable':
                raise serializers.ValidationError('Invalid email.')

        return email

    def enrich_account(self):
        data = self.validated_data

        email = data['email']

        if settings.CLEARBIT_API_KEY:
            response = clearbit_enrichment(email)

            name = response.get('name', {})
            data['first_name'] = '' if not name.get('givenName') \
                else name.get('givenName')
            data['last_name'] = '' if not name.get('familyName') \
                else name.get('familyName')

            data['location'] = response.get('location')
            data['bio'] = response.get('bio')
            data['site'] = response.get('site')
            data['avatar'] = response.get('avatar')
