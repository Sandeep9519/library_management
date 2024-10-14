from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book, BorrowRecord
from .permissions import IsLibrarian
from .serializers import BookSerializer, BorrowRecordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book, BorrowRecord
from .permissions import IsLibrarian
from .serializers import BookSerializer, BorrowRecordSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsLibrarian

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
          
            permission_classes = [IsAuthenticated, IsLibrarian]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]




@api_view(['POST'])
@permission_classes([AllowAny]) 
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role')

    if not username or not password or not role:
        return Response({"error": "Please provide all required fields (username, password, role)."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create(
            username=username,
            password=make_password(password),  
            is_staff=True if role == 'LIBRARIAN' else False  
        )

        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)