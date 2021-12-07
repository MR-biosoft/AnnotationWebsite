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
        # print(get_list_or_404(Genome, specie=request.POST.get("specie", "")))
        if "chromosome" in request.POST:
            chromosome = request.POST.get("chromosome", "")
            hits = get_list_or_404(Genome, chromosome__iexact = chromosome)
            context = {"hits": hits}
        elif "specie" in request.POST:
            # specie, strain, minsize, maxsize, motif = request.POST.get("specie", "strain", "minsize", "maxsize", "motif", "")
            specie = request.POST.get("specie", "")
            strain = request.POST.get("strain", "")
            motif = request.POST.get("motif", "")
            minsize = request.POST.get("minsize", "")
            maxsize = request.POST.get("maxsize", "")
            minsize = int(minsize) if minsize else minsize
            maxsize = int(maxsize) if maxsize else maxsize
            print(maxsize)
            print(type(maxsize))
            hits = Genome.objects
            # hits = get_list_or_404(Genome)
            # print("hits1 = ", hits)
            # hits = Genome.objects.filter(specie = specie) if specie else hits
            # hits = Genome.objects.filter(specie__icontains = specie) if specie else hits
            hits = hits.filter(specie__icontains = specie) if specie else hits
            hits = hits.filter(strain__iexact = strain) if strain else hits
            hits = hits.filter(sequence__icontains = motif) if motif else hits
            hits = hits.filter(length__gte = minsize) if minsize else hits
            hits = hits.filter(length__lte = maxsize) if maxsize else hits
            context = {"hits": hits}

        return render(request, self.POST_template, context)
