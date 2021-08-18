from django.utils import timezone
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo

# Auth: GET, POST
class TodoList(generics.ListCreateAPIView):
  serializer_class = TodoSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user

    return Todo.objects.filter(
      user=user, completed__isnull=True
    ).order_by('created')

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

# Auth: GET, PUT, DELETE
class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = TodoSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return Todo.objects.filter(user=user)

# Auth: GET, PUT, PATCH
class TodoComplete(generics.RetrieveUpdateAPIView):
  serializer_class = TodoCompleteSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return Todo.objects.filter(
      user=user, completed__isnull=True
    )

  def perform_update(self, serializer):
    serializer.instance.completed = timezone.now()
    serializer.save()

# Auth: GET, PUT, PATCH
class TodoRedo(generics.RetrieveUpdateAPIView):
  serializer_class = TodoCompleteSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    return Todo.objects.filter(
      user=user, completed__isnull=False
    )

  def perform_update(self, serializer):
    serializer.instance.completed = None
    serializer.save()

# Auth: GET
class TodoCompletedList(generics.ListAPIView):
  serializer_class = TodoSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user

    return Todo.objects.filter(
      user=user, completed__isnull=False
    ).order_by('-completed')
