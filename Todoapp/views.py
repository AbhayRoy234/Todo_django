from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
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
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentTodos')
            except IntegrityError:
                return render(request, 'Todoapp/signup.html', {'form': UserCreationForm, 'error': "Please choose Another username"})
        else:
            return render(request,'Todoapp/signup.html',{'form':UserCreationForm,'error':"password didn't Match"})

@login_required
def currentTodos(request):
    todo=Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'Todoapp/currentTodo.html',{'todo':todo})

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

@login_required
def createTodos(request):
    if request.method=="GET":
        return render(request, 'Todoapp/createTodos.html', {'form':TodoForm})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'Todoapp/currentTodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


def completetodo(todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)

    todo.datecompleted = timezone.now()
    todo.save()
    return redirect('currentTodos')

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'Todoapp/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            if 'complete' in request.POST:
                # print("hello")
                completetodo(todo_pk)
            elif '_delete' in request.POST:
                # print("hello")
                todo.delete()
            # print("hello")
            return redirect('currentTodos')
        except ValueError:
            return render(request, 'Todoapp/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})




@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentTodos')

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'Todoapp/completedtodos.html', {'todos':todos})