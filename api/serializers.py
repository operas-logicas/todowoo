from django.contrib.auth import get_user_model
from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
  created = serializers.ReadOnlyField()
  completed = serializers.ReadOnlyField()
  
  class Meta:
    model = Todo
    fields = ['id', 'title', 'memo', 'created', 'completed', 'important']
