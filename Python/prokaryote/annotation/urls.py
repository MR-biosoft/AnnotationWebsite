""" Main site functionality """

from django.urls import path
from . import views

urlpatterns = [
    # path("", views),
    # if we have a class-based view, we have to call  the .as_view() method
    path("genome", views.GenomeView.as_view(), name="genome"),
    # re_path(r"^genome/(?P<chromosome>)\w*$",
    # views.SingleGenomeView.as_view(), name="single_genome"),
    path("gene", views.GeneView.as_view(), name="gene"),
    path("protein", views.ProteinView.as_view(), name="protein"),
]
