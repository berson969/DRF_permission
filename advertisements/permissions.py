from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerOrIsStaffOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True

        # Instance must have an attribute named `owner`.
        return obj.creator == request.user
    

class IsNotOwner(permissions.BasePermission):
       
    def has_permission(self, request, view, obj):
        
        if request.method == 'GET' and obj.creator != request.user or request.user.is_staff:
            return True

       