from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Task  # Make sure to import the Task model
from .forms import TaskForm  # Ensure TaskForm is also imported if used in the dashboard view

def index(request):
    return render(request, 'todo/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after sign up
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'todo/dashboard.html', {'tasks': tasks, 'form': form})
