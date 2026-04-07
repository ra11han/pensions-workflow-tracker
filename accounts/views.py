"""Views that handle account creation and login handoff."""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


def register(request):
    """Create a new user account and sign in immediately after success."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        # Initialize an empty form for first-time page loads.
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
