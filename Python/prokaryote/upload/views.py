"""
"""

from django.shortcuts import render
from django.core import management

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

# IMPORT_KW_ARGS = {
#    "update": False,
#    "log_errors": True,
#    "catch_errors": False,
#    "verbose": False,
# }

# _import_genes = ParallelFASTAImporter(save_gene, **IMPORT_KW_ARGS)
# _import_proteins = ParallelFASTAImporter(save_protein)
#
#
# def handle_genome_file(genome_file):
#    """Wrapper to call save_genome"""
#    with open(genome_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
#        record = SeqIO.read(_tmp, "fasta")
#        save_genome(record)
#
#
# def handle_gene_file(gene_file):
#    """Wrapper to call save_genome"""
#    with open(gene_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
#        _skipped_entries = _import_genes(_tmp)
#    return _skipped_entries
#
#
# def handle_protein_file(protein_file):
#    """Wrapper to call save_genome"""
#    with open(protein_file.temporary_file_path(), "r", encoding="utf-8") as _tmp:
#        _skipped_entries = _import_proteins(_tmp)
#    return _skipped_entries


file_command_dict = {
    "genome": "importgenome",
    "genes": "importgenes",
    "proteins": "importproteins",
}


def upload_file(request):
    """ """

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            _file = request.FILES["file"]
            _type = request.POST["file_type"]
            if _type == "genome":
                management.call_command(
                    file_command_dict[_type],
                    _file.temporary_file_path(),
                    specie=request.POST["specie"],
                    strain=request.POST["strain"],
                )
            else:
                management.call_command(
                    file_command_dict[_type], _file.temporary_file_path()
                )

            return HttpResponseRedirect("/upload")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
