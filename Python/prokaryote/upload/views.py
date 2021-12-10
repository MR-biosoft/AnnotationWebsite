"""
"""
import multiprocessing as mp

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

from annotation.parsing import save_genome, save_gene, save_protein
from Bio import SeqIO


def handle_genome_file(genome_file):
    """Wrapper to call save_genome"""
    with open(genome_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
        record = SeqIO.read(_tmp, "fasta")
        save_genome(record)


def handle_gene_file(gene_file):
    """Wrapper to call save_genome"""
    with open(gene_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
        record = SeqIO.parse(_tmp, "fasta")


def handle_protein_file(genome_file):
    """Wrapper to call save_genome"""
    with open(genome_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
        record = SeqIO.parse(_tmp, "fasta")


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_genome_file(request.FILES["genome_file"])
            handle_genome_file(request.FILES["gene_file"])
            handle_genome_file(request.FILES["protein_file"])
            return HttpResponseRedirect("/upload")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
