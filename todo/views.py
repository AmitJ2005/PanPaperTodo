from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Task, Learning, Profile
from .forms import TaskForm, LearningForm, ProfileForm, UserForm
from django.utils import timezone
import datetime
from dateutil import parser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings


def index(request):
    return render(request, 'todo/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
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
    
    # Handle selected_date from form submission
    if request.method == 'POST':
        selected_date_str = request.POST.get('selected_date', current_date.strftime('%Y-%m-%d'))
        
    try:
        selected_date = parser.parse(selected_date_str).date()
    except ValueError:
        selected_date = current_date
    
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
            return redirect(f'{request.path}?task_date={selected_date}')
        else:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.due_date = selected_date
                task.save()
                return redirect(f'{request.path}?task_date={selected_date}')
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

@login_required
def profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if profile_form.is_valid():
            # Check if only profile picture is being updated
            if 'profile_picture' in request.FILES:
                new_profile = profile_form.save(commit=False)
                new_profile.profile_picture = request.FILES['profile_picture']
                new_profile.save(update_fields=['profile_picture'])
            else:
                # Update both user information and profile picture
                if user_form.is_valid():
                    user_form.save()
                profile_form.save()

            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        # Populate forms with initial data
        user_form = UserForm(instance=user, initial={'username': user.username, 'email': user.email})
        profile_form = ProfileForm(instance=profile)

    return render(request, 'todo/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'username': user.username, 
    })


@login_required
def delete_profile_picture(request):
    profile = request.user.profile
    if profile.profile_picture and profile.profile_picture.name != 'profile_pictures/default.png':
        # Delete the existing profile picture file
        profile.profile_picture.delete()
        # Set the profile picture field to None
        profile.profile_picture = None
        profile.save()
        messages.success(request, 'Profile picture deleted successfully!')
    else:
        messages.error(request, 'No profile picture to delete or already using default picture.')
    
    return redirect('profile')


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=user)
    
    context = {
        'form': form,
        'username': user.username,  # Add the username to the context
    }

    return render(request, 'todo/change_password.html', context)