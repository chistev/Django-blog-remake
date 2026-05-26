from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib import messages

from account.forms import CustomUserCreationForm

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'account/register.html', {'form':form})
