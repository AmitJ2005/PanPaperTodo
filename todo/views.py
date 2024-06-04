from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Task  # Make sure to import the Task model
from .forms import TaskForm  # Ensure TaskForm is also imported if used in the dashboard view
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import os

def index(request):
    return render(request, 'todo/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'todo/signup.html', {'form': form})



@login_required
def dashboard(request):
    current_date = timezone.now().date()
    min_date = current_date
    max_date = current_date + datetime.timedelta(days=30)
    
    selected_date_str = request.GET.get('task_date', current_date.strftime('%Y-%m-%d'))
    selected_date = datetime.datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    
    tasks = Task.objects.filter(user=request.user, due_date=selected_date)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.due_date = selected_date
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    
    context = {
        'tasks': tasks,
        'form': form,
        'current_date': current_date,
        'selected_date': selected_date,
        'min_date': min_date,
        'max_date': max_date,
    }

    # print("Looking for template at: ", os.path.join('todo_app', 'todo', 'templates', 'dashboard.html'))
    return render(request, 'todo/dashboard.html', context)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')
