from rest_framework import generics, permissions
from .serializers import TodoSerializer
from todo.models import Todo

# Auth: GET, POST
class TodoCompletedList(generics.ListCreateAPIView):
  serializer_class = TodoSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    
    return Todo.objects.filter(
      user=user, completed__isnull=False
    ).order_by('-completed')

# Auth: GET, PUT, DELETE
class TodoDetail(generics.RetrieveUpdateAPIView):
  pass

class TodoList(generics.ListAPIView):
  pass
