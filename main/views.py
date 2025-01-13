from django.shortcuts import render
from django.urls import reverse
import uuid
from .forms import ShareForm
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
                file.name = uuid.uuid4()
                file.file = form.cleaned_data["file"]
                file.file.name = str(file.name)
                file.save()
                link = request.build_absolute_uri("/" + str(file.name))
                return render(request, "success.html", {"link": link})
    else:
        form = ShareForm()
    return render(request, "share.html", {"form": form})
