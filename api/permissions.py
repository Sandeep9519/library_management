from rest_framework.permissions import BasePermission

class IsLibrarian(BasePermission):
    """
    Custom permission to only allow librarians to create, update, or delete books.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'LIBRARIAN'
