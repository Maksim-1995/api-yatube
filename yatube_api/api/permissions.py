from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешает изменение/удаление объекта только его автору."""

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем аутентифицированным
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
