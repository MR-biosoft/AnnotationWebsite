""" Custom forms for file handling """
from django import forms


class UploadFileForm(forms.Form):
    """Basic file form"""

    FILE_TYPE_CHOICES = (
        ("genome", "genome"),
        ("genes", "genes"),
        ("proteins", "proteins"),
    )

    genome_file = forms.FileField(required=True)
    gene_file = forms.FileField(required=True)
    protein_file = forms.FileField(required=True)
    # file_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES)


class UploadGenomeForm(UploadFileForm):
    """Form to upload a genome"""
