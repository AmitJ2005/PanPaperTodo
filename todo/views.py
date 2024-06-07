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
from .forms import LearningForm
from .models import Learning

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
    not_done_tasks = Task.objects.filter(user=request.user, completed=False).exclude(due_date=selected_date)
    learning = Learning.objects.filter(user=request.user, date=selected_date).first()
    
    if request.method == 'POST':
        if 'learning_content' in request.POST:
            learning_content = request.POST['learning_content']
            if learning:
                learning.content = learning_content
            else:
                learning = Learning(user=request.user, date=selected_date, content=learning_content)
            learning.save()
            return redirect('dashboard')
        else:
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
        'not_done_tasks': not_done_tasks,
        'learning_content': learning.content if learning else '',
    }

    return render(request, 'todo/dashboard.html', context)

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed  # Toggle completion status
    task.save()
    return redirect('dashboard')

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
