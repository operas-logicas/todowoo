from django.urls.conf import include
from api import views
from django.urls import include, path

urlpatterns = [
  path('api-auth', include('rest_framework.urls')),
  path('todos/', views.TodoList.as_view()),
  path('todos/<int:pk>/', views.TodoDetail.as_view()),
  path('todos/<int:pk>/complete', views.TodoComplete.as_view()),
  path('todos/<int:pk>/redo', views.TodoRedo.as_view()),
  path('todos/completed/', views.TodoCompletedList.as_view()),
]
