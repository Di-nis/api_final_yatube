from rest_framework.permissions import BasePermission


class OwnResourcePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in ['GET', 'OPTIONS', 'HEAD'] or
                obj.author == request.user)
