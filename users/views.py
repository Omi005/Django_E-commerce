from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(
        request,
        'users/signup.html',
        {'form': form}
    )


@login_required
def profile(request):
    profile = Profile.objects.get(
        user=request.user
    )

    return render(
        request,
        'users/profile.html',
        {
            'profile': profile
        }
    )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
    request.POST,
    request.FILES,
    instance=request.user.profile
)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect('profile')

    else:
        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=request.user.profile
        )

    return render(
        request,
        'users/edit_profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )