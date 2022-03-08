from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ScraperUser
from .logic.navigate import open_application as oa
import threading

def index(request):
    return render(request, 'navigate/index.html',{})

def users(request):
    return render(request, 'navigate/user.html',{})

def open_application(request):
    #user=get_object_or_404(ScraperUser, username=request.POST['login_name'])
    try:
        
        su=ScraperUser(username=request.POST['login_name'],password=request.POST['login_password'])
        su.save_user()
        oa.main(su.username)
        
    except (Exception):
        raise (Exception)
        

    return HttpResponse("Insertado")