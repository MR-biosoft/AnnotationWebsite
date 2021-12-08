""" Docstring """

from django import forms

# Imports from our App
from annotation.models import Genome


class GenomeForm(forms.ModelForm):
    class Meta:
        model = Genome
        fields = ["chromosome", "specie", "strain", "sequence", "length"]
