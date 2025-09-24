from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Subject, Badge, Profile
from .forms import TaskForm

def index_view(request):
    return render(request, 'core/index.html')

@login_required
def dashboard_view(request):
    # Handle the form submission
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the current user
            task.save()
            return redirect('dashboard') # Redirect to the same page to see the new task
    else:
        form = TaskForm(user=request.user)

    # Get all tasks for the current user to display
    tasks = Task.objects.filter(user=request.user)
    
    context = {
        'tasks': tasks,
        'form': form, # Add the form to the context
    }
    return render(request, 'core/dashboard.html', context)
        
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard') # <-- THIS IS THE FIX
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard') # <-- THIS IS THE FIX
    else:
        form = UserCreationForm()
    
    return render(request, 'core/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')

# Add this to your views.py file
@login_required
def subjects_view(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        if subject_name: # Make sure it's not empty
            Subject.objects.create(user=request.user, name=subject_name)
            return redirect('subjects')

    subjects = Subject.objects.filter(user=request.user)
    context = {
        'subjects': subjects,
    }
    return render(request, 'core/subjects.html', context)

@login_required
def delete_subject_view(request, subject_id):
    subject = Subject.objects.get(id=subject_id, user=request.user)
    subject.delete()
    return redirect('subjects')

@login_required
def complete_task_view(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    
    # Call the badge check function after saving
    check_and_award_badges(request.user)
    
    return redirect('dashboard')

@login_required
def delete_task_view(request, task_id):
    # Get the task by its ID and ensure it belongs to the logged-in user
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')

# core/views.py

def check_and_award_badges(user):
    profile = user.profile  # We can now access the profile directly
    
    # --- Workload Badges ---
    completed_tasks_count = Task.objects.filter(user=user, completed=True).count()
    
    # Badge: Task Novice (1 task)
    if completed_tasks_count >= 1:
        badge = Badge.objects.get(name="Task Novice")
        profile.badges.add(badge)

    # Badge: Task Slayer (10 tasks)
    if completed_tasks_count >= 10:
        badge = Badge.objects.get(name="Task Slayer")
        profile.badges.add(badge)

    # --- Consistency Badges ---
    # Badge: Getting Started (tasks on 2 different days)
    distinct_days = Task.objects.filter(user=user, completed=True).dates('created_at', 'day').count()
    if distinct_days >= 2:
        badge = Badge.objects.get(name="Getting Started")
        profile.badges.add(badge)

    profile.save()

@login_required
def achievements_view(request):
    profile = request.user.profile
    earned_badges = profile.badges.all()
    all_badges = Badge.objects.all() # Get all badges
    
    # Calculate progress
    earned_count = earned_badges.count()
    total_count = all_badges.count()
    progress_percentage = int((earned_count / total_count) * 100) if total_count > 0 else 0

    context = {
        'all_badges': all_badges,
        'earned_badges': earned_badges,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'core/achievements.html', context)