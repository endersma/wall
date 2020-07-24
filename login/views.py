from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):

    return render(request, 'login/index.html')

def create(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for field, value in errors.items():
             messages.error(request, value)
        return redirect('/')
    User.objects.register(request.POST)
    return redirect('/')

def login(request):
    auth = User.objects.authenticate(request.POST['email'], request.POST['password'])
    if auth == False:
        messages.error( request, "Invalid Credentials")
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/wall')
    return redirect('/')

def success(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'wall.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')