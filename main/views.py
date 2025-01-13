from django.shortcuts import render
from django.urls import reverse
import uuid
from .forms import ShareForm, LoginForm
from .models import UserFile

def mainView(request):
    return render(request, "main.html")

def shareView(request):
    if request.method == "POST":
            form = ShareForm(request.POST, request.FILES)
            if form.is_valid():
                if (form.cleaned_data["accesspwd1"] != form.cleaned_data["accesspwd2"] or
                    form.cleaned_data["deletionpwd1"] != form.cleaned_data["deletionpwd2"]):
                    return render(request, "share.html", {"form": form, "errormsg": "Passwords do not match"})
                file = UserFile()
                file.accesspwd = form.cleaned_data["accesspwd1"]
                file.deletionpwd = form.cleaned_data["deletionpwd1"]
                file.id = uuid.uuid4()
                file.file = form.cleaned_data["file"]
                file.file.name = str(file.id)
                file.save()
                link = request.build_absolute_uri("/" + str(file.id))
                return render(request, "success.html", {"link": link})
    else:
        form = ShareForm()
    return render(request, "share.html", {"form": form})

def fileView(request, uid_str):
    if request.method == "POST":
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
        form = LoginForm
    return render(request, "login.html", {"form": form})
