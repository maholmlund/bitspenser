from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseNotAllowed
import uuid
from .forms import ShareForm, LoginForm
from .models import UserFile

def mainView(request):
    if request.method == "GET":
        return render(request, "main.html")
    else:
        return HttpResponseNotAllowed()

def shareView(request):
    if request.method == "GET":
        return render(request, "share.html", {"form": ShareForm()})
    elif request.method == "POST":
        form = ShareForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "share.html", {"form": form})
        if (form.cleaned_data["accesspwd1"] != form.cleaned_data["accesspwd2"] or
            form.cleaned_data["deletionpwd1"] != form.cleaned_data["deletionpwd2"]):
            return render(request, "share.html", {"form": form, "errormsg": "Passwords do not match"})
        userfile = UserFile()
        userfile.accesspwd = form.cleaned_data["accesspwd1"]
        userfile.deletionpwd = form.cleaned_data["deletionpwd1"]
        userfile.id = uuid.uuid4()
        userfile.file = form.cleaned_data["file"]
        userfile.file.name = str(userfile.id)
        userfile.save()
        link = request.build_absolute_uri("/" + str(userfile.id))
        return render(request, "success.html", {"link": link})
    else:
        return HttpResponseNotAllowed()

def fileView(request, uid_str):
    if request.method == "GET":
        return render(request, "login.html", {"form": LoginForm()})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "login.html", {"form": form, "errormsg": "Invalid link or password"})
        uid = None
        try:
            uid = uuid.UUID(uid_str)
        except ValueError:
            pass
        file = UserFile.objects.filter(id=uid)
        if not file:
            return render(request, "login.html", {"form": form, "errormsg": "Invalid link or password"})
        file = file[0]
        if file.accesspwd != form.cleaned_data["passwd"] and file.deletionpwd != form.cleaned_data["passwd"]:
            return render(request, "login.html", {"form": form, "errormsg": "Invalid link or password"})
        # TODO: show file
    else:
        return HttpResponseNotAllowed()
