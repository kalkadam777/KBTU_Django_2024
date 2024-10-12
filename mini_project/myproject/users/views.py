from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Follow
from .forms import UserRegisterForm
from django.contrib import messages
from .forms import ProfileForm 

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    # profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправляем на страницу профиля после успешного сохранения
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'users/edit_profile.html', {'form': form})