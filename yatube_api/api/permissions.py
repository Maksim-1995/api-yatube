from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение на редактирование только для автора."""

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем редактирование только автору
        return obj.author == request.user
