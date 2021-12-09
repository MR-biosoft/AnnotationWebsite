from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

from annotation.parsing import save_genome
from Bio import SeqIO


def handle_uploaded_file(f):
    print()
    print(type(f))
    print(type(f.file))
    print()
    print(dir(f))
    print()
    # f:
    with open(f.temporary_file_path(), "r", encoding="utf-8") as _tmp:
        record = SeqIO.read(_tmp, "fasta")
        save_genome(record)
    # with open("beepboop.txt", "wb+") as destination:
    #    for chunk in f.chunks():
    #        destination.write(chunk)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/upload")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
