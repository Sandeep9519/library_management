from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    LIBRARIAN = 'LIBRARIAN'
    MEMBER = 'MEMBER'

    ROLE_CHOICES = [
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Avoid conflict with auth.User.groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Avoid conflict with auth.User.user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class Book(models.Model):
    AVAILABLE = 'AVAILABLE'
    BORROWED = 'BORROWED'

    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (BORROWED, 'Borrowed'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=AVAILABLE)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
