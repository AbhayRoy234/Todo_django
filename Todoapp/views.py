from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# from .forms import TodoForm
# from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'Todoapp/home.html')
def signUpUser(request):
    if request.method== "GET":
        return render(request,'Todoapp/signup.html',{'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentTodos')
            except IntegrityError:
                return render(request, 'Todoapp/signup.html', {'form': UserCreationForm, 'error': "Please choose Another username"})
        else:
            return render(request,'Todoapp/signup.html',{'form':UserCreationForm,'error':"password didn't Match"})


def currentTodos(request):
    return render(request,'Todoapp/currentTodo.html')

def logoutuser(request):
    if request.method=="POST":
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'Todoapp/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'Todoapp/login.html',{'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currentTodos')



