from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.hashers import check_password

def delete(req):
    pwck = req.POST.get("pwck")
    if check_password(pwck, req.user.password):
        req.user.pic.delete()
        req.user.delete()
        return redirect("acc:index")
    else:
        # 메세지 출력
        return redirect("acc:profile")

def update(req):
    if req.method == "POST":
        u = req.user
        ue = req.POST.get("umail")
        up = req.POST.get("upass")
        ua = req.POST.get("uage")
        pi = req.FILES.get("upic")
        uc = req.POST.get("ucom")
        if up:
            u.set_password(up)
        u.email = ue
        u.age = ua
        if pi:
            u.pic.delete()
            u.pic = pi
        u.comment = uc
        u.save()
        login(req, u)
        return redirect("acc:profile")
        
    return render(req, "acc/update.html")

def profile(req):
    return render(req, "acc/profile.html")

def signup(req):
    if req.method == "POST":
        un = req.POST.get("uname")
        up = req.POST.get("upass")
        ua = req.POST.get("uage")
        pi = req.FILES.get("upic")
        uc = req.POST.get("ucom")
        try:
            User.objects.create_user(username=un, password=up, age=ua, pic=pi, comment=uc)
            return redirect("acc:login")
        except:
            pass # 메시지 넣을곳!
    return render(req, "acc/signup.html")

def logout_user(req):
    logout(req)
    return redirect("acc:login")

def index(req):
    return render(req, "acc/index.html")

def login_user(req):
    if req.method == "POST":
        un = req.POST.get("uname")
        up = req.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u:
            login(req, u)
            return redirect("acc:index")
        else:
            pass # 메세지할것!!
    return render(req, "acc/login.html")