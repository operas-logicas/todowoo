from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.shortcuts import redirect, render

# Create your views here.
def currenttodos(request):
  return render(
    request,
    'todo/current.html'
  )

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
          request.POST['username'],
          request.POST['password1']
        )

        # Save & login new user
        user.save()
        login(request, user)

        # Redirect to currenttodos/
        return redirect('currenttodos')

      except IntegrityError:
        error = 'Username already taken! Please choose a new username.'

        return render(
          request,
          'todo/signup.html',
          { 'form': UserCreationForm(), 'error': error }
        )

  else:
    # GET request so send sign up form
    return render(
      request,
      'todo/signup.html',
      { 'form': UserCreationForm() }
    )
