from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainView),
    path("share/", views.shareView),
    path("share", views.shareView),
    path("download/<uid_str>", views.downloadView),
    path("delete/<uid_str>", views.deleteView),
    path("<uid_str>", views.unlockView),
]
