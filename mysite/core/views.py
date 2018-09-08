from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'core/signup.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Plz enter valid data in your form")
        form.save()
        user = User.objects.get(username=form.cleaned_data.get('username'))
        #password = User.objects.get(password=form.cleaned_data.get('password'))
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
        #password = request.password.password
        return HttpResponse("Login \t" + username)
def login_user(request):
    if request.method == 'GET':
        return render(request, 'core/login.html')
    elif request.method == 'POST':
        if request.method == 'POST':
            username = request.POST['user_name']
            password = request.POST['user_password']
            print(username)
            print(password)
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    #login(request, user)
                    return HttpResponse('welcome\t'+username)
                else:
                    return HttpResponse("Your Rango account is disabled.")
            else:
                return HttpResponse("Invalid login details supplied.")
        else:
            return render_to_response('core/login.html', {}, context)



