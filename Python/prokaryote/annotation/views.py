"""
Docstring
"""
from django.views import View
from django.shortcuts import render, get_object_or_404, get_list_or_404

from annotation.models import Genome
from annotation.forms import GenomeForm


def something(request):
    pass


# Create your views here.
class GenomeView(View):
    """Manage logic to the genome view"""

    GET_template = "genome_form.html"
    POST_template = "genome_query.html"

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
        print("-------------------Test---------------------")
        print(request.POST.keys())
        print(request.POST)
        #print(get_object_or_404(Genome, specie=request.POST.get("specie", "")))
        print("get_list_or_404")
        print(get_list_or_404(Genome, specie=request.POST.get("specie", "")))
        if "chromosome" in request.POST:
            chromosome = request.POST.get("chromosome", "")
            hits = get_list_or_404(Genome, chromosome = chromosome)
            context = {"hits": hits}
            """genome = get_list_or_404(
                Genome, chromosome=request.POST.get("chromosome", "")
            )
            context = {"chromosome": genome.chromosome, "specie": genome.specie, "strain": genome.strain, "length": genome.length}"""
        elif "specie" in request.POST:
            """hits = get_list_or_404(Genome, chromosome = 'ASM584v2')
            context = {"hits": hits}"""
            specie = request.POST.get("specie", "")
            hits = get_list_or_404(Genome, specie = specie)
            context = {"hits": hits}
            # context = {"specie" : "Theo", "strain" : "Gus"}

        return render(request, self.POST_template, context)
