"""
Docstring
"""
from django.views import View
from django.shortcuts import render, get_object_or_404

from annotation.models import Genome
from annotation.forms import GenomeForm


def something(request):
    pass


# Create your views here.
class GenomeView(View):
    """Manage logic to the genome view"""

    GET_template = "genome_form.html"
    POST_template = "basic.html"

    def get(self, request):
        """Method used to process GET requests"""
        # The dict's keys should be valid Python identifiers :
        # a combination of numbers, letters, and underscores, starting with a letter
        context = {"name": "value", "x": 5, "y": 17}
        return render(request, self.GET_template, context)

    def post(self, request):
        """Method used to process POST requests"""
        # form = GenomeForm(request.POST)
        # if form.is_valid():
        print(request.POST.keys())
        if "chromosome" in request.POST:
            genome = get_object_or_404(
                Genome, chromosome=request.POST.get("chromosome", "")
            )
            context = {"chromosome": genome.chromosome, "specie": genome.specie, "strain": genome.strain, "length": genome.length}
        elif "specie" in request.POST:
            context = {"specie" : "Theo", "strain" : "Gus"}

        return render(request, self.POST_template, context)
