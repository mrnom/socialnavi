from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_anonymous
        return request.user.is_authenticated


class IsCurrentUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user
