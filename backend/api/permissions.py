from rest_framework.permissions import BasePermission


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'role', None) == 'organizer'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'is_authenticated', False) and getattr(request.user, 'role', None) == 'admin'


class IsEventOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj.organizer is an Organizer instance; compare its user to the request user
        return getattr(getattr(obj, 'organizer', None), 'user', None) == getattr(request, 'user', None)