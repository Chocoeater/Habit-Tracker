from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешение на редактирование только для владельца или админа"""

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS для всех аутентифицированных
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для остальных методов проверяем владельца или админа
        return obj == request.user or request.user.is_staff
