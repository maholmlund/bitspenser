from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainView),
    path("share/", views.shareView),
    path("share", views.shareView),
    path("<uid_str>", views.fileView),
]
