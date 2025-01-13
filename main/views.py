from django.shortcuts import render

def mainView(request):
    return render(request, "main.html")

def shareView(request):
    return render(request, "share.html")

