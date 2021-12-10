""" Custom forms for file handling """
from django import forms


class UploadFileForm(forms.Form):
    """Basic file form"""

    FILE_TYPE_CHOICES = (
        ("genome", "genome"),
        ("genes", "genes"),
        ("proteins", "proteins"),
    )

    file = forms.FileField(required=True)
    specie = forms.CharField(max_length=20, required=False)
    strain = forms.CharField(max_length=20, required=False)
    # gene_file = forms.FileField(required=True)
    # protein_file = forms.FileField(required=True)
    file_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES)


class UploadGenomeForm(UploadFileForm):
    """Form to upload a genome"""
