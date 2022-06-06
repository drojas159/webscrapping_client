from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .logic.navigate import open_application as oa
import threading
base_url = "https://www.instagram.com/"
def index(request):
    return render(request, 'navigate/index.html',{})

def users(request):
    return render(request, 'navigate/user.html',{})

def open_application(request):
    #user=get_object_or_404(ScraperUser, username=request.POST['login_name'])
    try:        
        su=ScraperUser(username=request.POST['login_name'],password=request.POST['login_password'])
        u=User(username=request.POST['login_name'],profile_url=base_url+request.POST['login_name'])
        action_type = request.POST['action_type']
        su.save_user()
        u.save_user()
        oa.main(su.username, action_type)        
    except (Exception) as err:
        print(f"Unexpected {err=}, {type(err)=}")       

    return HttpResponse("Insertado")

def publications(request):
    return render(request, 'navigate/publication.html',{})

def comments(request):
    return render(request, 'navigate/comments.html',{})