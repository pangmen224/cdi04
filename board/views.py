from django.shortcuts import render,redirect
from .models import Board
from django.utils import timezone
# Create your views here.
def update(req, bpk):
    b = Board.objects.get(id=bpk)

    if req.user != b.writer:
        pass # 경고!!
        return redirect("board:index")

    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b": b
    }
    return render(req, "board/update.html", context)

def create(req):
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        t = timezone.now()
        Board(subject=s, writer=req.user, content=c, pubdate=t).save()
        return redirect("board:index")
    return render(req, "board/create.html")


def delete(req, bpk):
    b = Board.objects.get(id=bpk)
    if req.user == b.writer:
        b.delete()
    else:
        pass #메세지 넣을곳!!

    return redirect("board:index")

def detail(req, bpk):
    b = Board.objects.get(id=bpk)
    context = {
        "b" : b
    }
    return render(req, "board/detail.html", context)

def index(req):
    b = Board.objects.all()
    context = {
        "bset": b
    }
    return render(req, "board/index.html", context)

