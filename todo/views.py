from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import TodoForm
from .models import Todo

User = get_user_model()

# Create your views here.
def home(request):
  return render(request, 'todo/home.html')

def signupuser(request):
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    # Validate form
    form = UserCreationForm(request.POST)

    if form.is_valid():
      # Create new user
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password1']
      )

      # Save & login new user
      user.save()
      login(request, user)

      # Redirect to /currenttodos/
      return redirect('currenttodos')

    else:
      # Form validation failed
      messages.error(request, form.errors.as_ul())
      
      return render(
        request,
        'todo/signup.html',
        { 'form': UserCreationForm(), 'user': request.POST }
      )

  else:
    # GET request so return sign up form
    return render(
      request,
      'todo/signup.html',
      { 'form': UserCreationForm() }
    )

def loginuser(request):
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':    
    # Validate username & password
    user = authenticate(
      request,
      username = request.POST['username'],
      password = request.POST['password']
    )

    # Invalid username and/or password
    if user is None or not user.is_active:
      error = 'Invalid username and password!'

      return render(
        request,
        'todo/login.html',
        { 'form': AuthenticationForm(), 'error': error }
      )
    
    else:
      # Success!
      login(request, user)
      if request.GET.get('next', False):
        next = request.GET['next']
        return redirect(next)
      else: return redirect('currenttodos')

  else:
    # GET request so return login form
    return render(
      request,
      'todo/login.html',
      { 'form': AuthenticationForm() }
    )

@login_required
def logoutuser(request):
  if request.method == 'POST':
    logout(request)
    return redirect('home')
  else: return redirect('home')

@login_required
def createtodo(request):
  if request.method == 'POST':
    form = TodoForm(request.POST)

    if form.is_valid():
      todo = form.save(commit=False)
      todo.user = request.user
      todo.save()

      return redirect('currenttodos')

    else:
      error = 'Invalid data!'

      return render(
        request,
        'todo/create.html',
        { 'form': TodoForm, 'error': error }
      )
    
  else:
    # GET request so return create todo form
    return render(
      request,
      'todo/create.html',
      { 'form': TodoForm() }
    )

@login_required
def currenttodos(request):
  todos = Todo.objects.filter(user=request.user, completed__isnull=True)

  return render(
    request,
    'todo/current.html',
    { 'todos': todos }
  )

@login_required
def completedtodos(request):
  todos = Todo.objects.filter(
    user=request.user, completed__isnull=False
  ).order_by('-completed')

  return render(
    request,
    'todo/completed.html',
    { 'todos': todos }
  )

@login_required
def viewtodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

  if request.method == 'POST':
    updatedForm = TodoForm(request.POST, instance=todo)

    if updatedForm.is_valid():
      updatedForm.save()
      if todo.completed:
        return redirect('completedtodos')
      else:
        return redirect('currenttodos')

    else:
      form = TodoForm(instance=todo)
      error = 'Invalid data!'

      return render(
        request,
        'todo/todo.html',
        { 'todo': todo, 'form': form, 'error': error }
      )

  else:
    # GET request so return todo
    form = TodoForm(instance=todo)

    return render(
      request,
      'todo/todo.html',
      { 'todo': todo, 'form': form }
    )

@login_required
def completetodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

  if request.method == 'POST':
    todo.completed = timezone.now()
    todo.save()
    return redirect('currenttodos')
  else: return redirect('home')

@login_required
def deletetodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

  if request.method == 'POST':
    todo.delete()
    return redirect('currenttodos')
  else: return redirect('home')

@login_required
def redotodo(request, todo_pk):
  todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

  if request.method == 'POST':
    todo.completed = None
    todo.save()
    return redirect('currenttodos')
  else: return redirect('home')
