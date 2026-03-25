from rest_framework.permissions import BasePermission


class IsOwnerOrSharedReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return obj.owner == request.user or obj.shared_with.filter(id=request.user.id).exists()
        return obj.owner == request.user
