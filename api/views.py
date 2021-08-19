from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from .serializers import TodoSerializer, TodoCompleteSerializer
from todo.models import Todo

User = get_user_model()

# Auth Views

@csrf_exempt
def login(request):
  if request.method == 'POST':
    # Get the data
    data = JSONParser().parse(request)

    # Validate username & password
    user = authenticate(
      request,
      username=data['username'],
      password=data['password']
    )

    # Invalid username and/or password
    if user is None or not user.is_active:
      return JsonResponse(
        { 'error': 'Invalid username and/or password!' },
        status=401
      )

    else:
      # Success!
      try:
        token = Token.objects.get(user=user)
      except:
        token = Token.objects.create(user=user)
      finally:
        return JsonResponse(   
          { 'token': token.key },
          status=200
        )

@csrf_exempt
def signup(request):
  if request.method == 'POST':
    try:
      # Get the data
      data = JSONParser().parse(request)

      # Create new user
      user = User.objects.create_user(
        username=data['username'],
        password=data['password']
      )
      user.save()

      # Create token for user
      token = Token.objects.create(user=user)

      # Return response
      return JsonResponse(
        { 'token': token.key },
        status=201
      )
    
    except IntegrityError:
      return JsonResponse(
        { 'error': 'Username already taken!' },
        status=400
      )

# ------------------------------------------

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
