from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from . forms import SignupForm, EditProfileForm

def home(request):
	return render(request, 'authapp/home.html', {})


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(redirect, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('Logged in successfully!'))
			return redirect('home')
		else:
			messages.success(request, ('Wrong username or password!'))
			return redirect('login')
	else:
		return render(request, 'authapp/login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ('Logged out successfully!'))
	return redirect('login')


def register_user(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(redirect, username=username, password=password)
			login(request, user)
			messages.success(request, ('Registered successfully!'))
			return redirect('home')
	else:
		form = SignupForm()

	context = {'form': form}
	return render(request, 'authapp/register.html', context)


def edit_profile(request):
	if request.method == "POST":     # instance=request.user is passing user info
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('Profile updated successfully!'))
			return redirect('home')
	else:
		form = EditProfileForm(instance=request.user)

	context = {'form': form}
	return render(request, 'authapp/edit_profile.html', context)


def change_password(request):
	if request.method == "POST":   # data and user are for password page specific
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('Your password updated successfully!'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)

	context = {'form': form}
	return render(request, 'authapp/change_password.html', context)
