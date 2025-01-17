from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseNotAllowed, HttpResponse
import uuid
import datetime
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

def try_get_file(uid_str):
    uid = None
    try:
        uid = uuid.UUID(uid_str)
    except ValueError:
        return None
    file = UserFile.objects.filter(id=uid)
    if not file:
        return None
    return file[0]

def unlockView(request, uid_str):
    if request.method == "GET":
        file = try_get_file(uid_str)
        if (uid_str in request.session and file is not None and
            datetime.datetime.now() - datetime.datetime.fromisoformat(request.session[uid_str][0]) < datetime.timedelta(seconds=60)):
            return fileView(request, file, request.session[uid_str][1])
        else:
            return render(request, "login.html", {"form": LoginForm()})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "login.html", {"form": form, "errormsg": "Invalid link or password"})
        file = try_get_file(uid_str)
        if file is None:
            return render(request, "login.html", {"form": form, "errormsg": "Invalid link or password"})
        if file.deletionpwd == form.cleaned_data["passwd"]:
            request.session[uid_str] = (datetime.datetime.now().isoformat(), True)
        elif file.accesspwd == form.cleaned_data["passwd"]:
            request.session[uid_str] = (datetime.datetime.now().isoformat(), False)
        else:
            return render(request, "login.html", {"form": form, "errormsg": "Invalid link or password"})
        return redirect("/" + uid_str)
    else:
        return HttpResponseNotAllowed()

def bytes_to_str(n):
    if n // 1024 == 0:
        return str(n) + " bytes"
    elif n // 1024 ** 2 == 0:
        return f"{(n / 1024):.2f} kB"
    elif n // 1024 ** 3 == 0:
        return f"{(n / 1024 ** 2):.2f} MB"
    else:
        return f"{(n / 1024 ** 3):.2f} GB"

def fileView(request, file, can_delete):
    size = bytes_to_str(file.file.size)
    return render(request, "file.html", {"date": file.uploaded_at, "size": size, "uuid": str(file.id), "can_delete": can_delete})

def downloadView(request, uid_str):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    userfile = try_get_file(uid_str)
    if userfile is None or datetime.datetime.now() - datetime.datetime.fromisoformat(request.session[uid_str]) > datetime.timedelta(seconds=60):
        return redirect("/" + uid_str)
    data = userfile.file.read()
    return HttpResponse(data, "")

def deleteView(request, uid_str):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if uid_str not in request.session:
        return redirect("/" + uid_str)
    if not request.session[uid_str][1]:
        return redirect("/" + uid_str)
    file = try_get_file(uid_str)
    file.delete()
    return redirect("/")
