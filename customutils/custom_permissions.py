from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

__author__ = 'goutom roy'

class IsAnonymousUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return True

