"""
"""

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

from annotation.parsing import (
    save_genome,
    save_gene,
    save_protein,
    ParallelFASTAImporter,
)
from Bio import SeqIO

IMPORT_KW_ARGS = {
    "update": False,
    "log_errors": True,
    "catch_errors": False,
    "verbose": False,
}

_import_genes = ParallelFASTAImporter(save_gene, **IMPORT_KW_ARGS)
_import_proteins = ParallelFASTAImporter(save_protein)


def handle_genome_file(genome_file):
    """Wrapper to call save_genome"""
    with open(genome_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
        record = SeqIO.read(_tmp, "fasta")
        save_genome(record)


def handle_gene_file(gene_file):
    """Wrapper to call save_genome"""
    with open(gene_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
        _skipped_entries = _import_genes(_tmp)
    return _skipped_entries


def handle_protein_file(protein_file):
    """Wrapper to call save_genome"""
    with open(protein_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
        _skipped_entries = _import_proteins(_tmp)
    return _skipped_entries


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # print(type(request.FILES["genome_file"]))
            # handle_genome_file(request.FILES["genome_file"])
            # print(type(request.FILES["gene_file"]))
            # _parsed_genes_n_errors = handle_gene_file(request.FILES["gene_file"])
            print(type(request.FILES["protein_file"]))
            _parsed_protein_n_errors = handle_protein_file(
                request.FILES["protein_file"]
            )
            return HttpResponseRedirect("/upload")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
