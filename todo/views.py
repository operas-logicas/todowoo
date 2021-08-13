from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import IntegrityError
from django.shortcuts import redirect, render
from .forms import TodoForm

User = get_user_model()

# Create your views here.
def home(request):
  return render(request, 'todo/home.html')

def signupuser(request):
  if request.method == 'POST':
    # Validate password
    if request.POST['password1'] != request.POST['password2']:
      error = 'Password confirmation must match password!'

      return render(
        request,
        'todo/signup.html',
        { 'form': UserCreationForm(), 'error': error }
      )

    # Try creating new user
    else:
      try:
        user = User.objects.create_user(
          username = request.POST['username'],
          password = request.POST['password1']
        )

        # Save & login new user
        user.save()
        login(request, user)

        # Redirect to /currenttodos/
        return redirect('currenttodos')

      except IntegrityError:
        error = 'Username already taken! Please choose a new username.'

        return render(
          request,
          'todo/signup.html',
          { 'form': UserCreationForm(), 'error': error }
        )

  else:
    # GET request so return sign up form
    return render(
      request,
      'todo/signup.html',
      { 'form': UserCreationForm() }
    )

def loginuser(request):
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
      return redirect('currenttodos')

  else:
    # GET request so return login form
    return render(
      request,
      'todo/login.html',
      { 'form': AuthenticationForm() }
    )

def logoutuser(request):
  if request.method == 'POST':
    logout(request)
    return redirect('home')
  else: return redirect('home')

def createtodo(request):
  if not request.user.is_authenticated:
    return redirect('loginuser')

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

def currenttodos(request):
  return render(
    request,
    'todo/current.html'
  )
