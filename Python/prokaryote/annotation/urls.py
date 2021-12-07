""" Main site functionality """

from django.urls import path
from . import views

urlpatterns = [
    # path("", views),
    # if we have a class-based view, we have to call  the .as_view() method
    path("genome", views.GenomeView.as_view(), name="genome"),
    path("gene", views.GeneView.as_view(), name="gene"),
]
