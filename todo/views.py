from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'POST':
        # Create new user
        if request.POST.get('password1', False) == request.POST.get('password2', False):
            try:
                user = User.objects.create_user(request.POST.get('username', False),
                                                password=request.POST.get('password1', False))
                user.save()
                login(request, user)  # log into user
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'Username is already taken'})
            except ValueError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'Invalid data'})
        else:
            # tell user passwords don't match
            print('error dont match')
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                            'error': 'Passwords dont match'})
    return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})


def loginuser(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),
                                                           'error': 'Username or password incorrect'})
        else:
            login(request, user)  # log into user
            return redirect('currenttodos')

    return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})


@login_required
def logoutuser(request):
    if request.method == 'POST':  # important so that browsers wont load this page if you are logged in
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(),
                                                            'error': 'Data is not valid'})
    return render(request, 'todo/createtodo.html', {'form': TodoForm()})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=True).order_by('-important', '-creation_date')
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=False).order_by('-completed_date')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):              # user=request.user to prevent other user from accessing your todos
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)  # looking in class Todoo, pk = primary key in DB
    if request.method == 'POST':
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            form = TodoForm(instance=todo)
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Data is not valid'})
    form = TodoForm(instance=todo)  # to make form show up and make it being filled with an existing info already
    return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completed_date = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
