from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором."""

    message = "Adding customers not allowed."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    message = "Доступ разрешен только владельцу."

    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'owner') and obj.owner == request.user
