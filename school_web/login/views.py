from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AdminLoginForm

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('home:home')

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('home:home')
            else:
                messages.error(request, 'Kredensial login tidak valid atau Anda tidak memiliki izin yang cukup.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'login/admin_login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('home:home')  # Redirect ke halaman login setelah logout