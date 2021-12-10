""" Custom forms for file handling """
from django import forms


class UploadFileForm(forms.Form):
    """Basic file form"""

    # genome_file = forms.FileField(required=True)
    # gene_file = forms.FileField(required=True)
    protein_file = forms.FileField(required=True)


class UploadGenomeForm(UploadFileForm):
    """Form to upload a genome"""
