from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'core/signup.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return HttpResponse("hello....")
        form.save()
        user = User.objects.get(username=form.cleaned_data.get('username'))
        login(request, user)
        return HttpResponse("User is created")
    else:
       return HttpResponse("unsupported method")
        ##form = UserCreationForm()
    #return render(request, 'signup.html', {'form': form})

def print_user(request):
    if request.user.is_anonymous:
        return HttpResponse("Not Login")
    else:
        username = request.user.username
        return HttpResponse("Login" + username)
