""" Docstring """

from django.urls import path
from annotation import views

urlpatterns = [
    # path("", views),
    # if we have a class-based view, we have to call  the .as_view() method
    path("genome", views.GenomeView.as_view(), name="genome"),
    # if we have a function-based view, we simply provide the name
    path("profile", views.something),
]
