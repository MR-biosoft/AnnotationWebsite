""" Home page and login """

from django.urls import path, re_path
from . import views

urlpatterns = [
    # path("", views),
    # if we have a class-based view, we have to call  the .as_view() method
    path("", views.HomeView.as_view(), name="menu"),
]
