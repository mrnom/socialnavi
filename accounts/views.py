from rest_framework import viewsets

from accounts.models import User
from accounts.permissions import IsAnonymous, IsCurrentUser
from accounts.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAnonymous, IsCurrentUser]

    @staticmethod
    def _hash_password(serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    def perform_create(self, serializer):
        serializer.verify_email()
        serializer.enrich_account()
        self._hash_password(serializer)

    def perform_update(self, serializer):
        self._hash_password(serializer)
