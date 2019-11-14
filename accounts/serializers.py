from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users-detail')
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['url', 'email', 'password']
