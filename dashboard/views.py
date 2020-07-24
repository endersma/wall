from django.shortcuts import render, redirect
from login.models import User
from .models import *

# Create your views here.
def wall(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'messages': Messages.objects.all(),
        }
    return render(request, 'dashboard/wall.html', context)

def create(request):
    Messages.objects.create(
        message=request.POST['message'],
        poster=User.objects.get(id=request.session['user_id']),
    )
    return redirect('/wall')

def create_comment(request, id):
    Comments.objects.create(
        comment=request.POST['comment'],
        message=Messages.objects.get(id=id),
        poster=User.objects.get(id=request.session['user_id']),
    )
    return redirect('/wall')

def delete(request, id):
    comment = Comments.objects.get(id=id)
    comment.delete()
    return redirect('/wall')

