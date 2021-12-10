"""
Views for main site
"""
from django.views import View
from django.shortcuts import render, get_list_or_404, get_object_or_404

from .models import Genome, GeneProtein
from .biopython import launch_blast

# Create your views here.
class GenomeView(View):
    """Manage logic to the genome view"""

    GET_template = "genome_form.html"
    POST_template = "genome_query.html"
    ENTRY_template = "single_genome_entry.html"

    def get(self, request):
        """Method used to process GET requests"""
        if "chromosome" in request.GET:
            chromosome = request.GET["chromosome"]
            entry = get_object_or_404(Genome, chromosome=chromosome)
            context = {"entry": entry}
            return render(request, self.ENTRY_template, context)
        else:
            return render(request, self.GET_template, {})

    def post(self, request):
        """Method used to process POST requests"""
        if "chromosome" in request.POST:
            chromosome = request.POST.get("chromosome", "")
            hits = get_list_or_404(Genome, chromosome__istartswith=chromosome)
            context = {"hits": hits}
        elif "specie" in request.POST:
            specie = request.POST.get("specie", "")
            strain = request.POST.get("strain", "")
            minsize = request.POST.get("minsize", "")
            maxsize = request.POST.get("maxsize", "")
            minsize = int(minsize) if minsize else minsize
            maxsize = int(maxsize) if maxsize else maxsize
            motif = request.POST.get("motif", "")
            hits = Genome.objects
            hits = hits.filter(specie__icontains=specie) if specie else hits
            hits = hits.filter(strain__iexact=strain) if strain else hits
            hits = hits.filter(sequence__icontains=motif) if motif else hits
            hits = hits.filter(length__gte=minsize) if minsize else hits
            hits = hits.filter(length__lte=maxsize) if maxsize else hits
            context = {"hits": hits}
        return render(request, self.POST_template, context)


class GeneView(View):
    """Manage logic to the gene view"""

    GET_template = "gene_form.html"
    POST_template = "gene_query.html"
    ENTRY_template = "single_gene_entry.html"
    BLAST_template = "BLAST_template.html"

    def get(self, request):
        """Method used to process GET requests"""
        if "gene" in request.GET:
            accession_number = request.GET["gene"]
            entry = get_object_or_404(
                GeneProtein.objects.select_related("chromosome")
                .select_related("annotation")
                .select_related("geneseq"),
                accession_number=accession_number,
            )
            context = {"entry": entry}
            return render(request, self.ENTRY_template, context)
        else:
            return render(request, self.GET_template, {})

    def post(self, request):
        """Method used to process POST requests"""
        context = {"hits": []}

        # Search by accession number
        if "ac" in request.POST:
            accession_number = request.POST.get("ac", "")
            hits = GeneProtein.objects
            hits = hits.filter(accession_number__istartswith=accession_number)
            hits = hits.select_related("chromosome").select_related("annotation")
            context = {"hits": hits} if hits.count() < 100 else {"hits": hits[:100]}
        # Search using multiple filters
        elif "chromosome" in request.POST:
            chromosome = request.POST.get("chromosome", "")
            specie = request.POST.get("specie", "")
            strain = request.POST.get("strain", "")
            minsize = request.POST.get("minsize", "")
            maxsize = request.POST.get("maxsize", "")
            minsize = int(minsize) if minsize else minsize
            maxsize = int(maxsize) if maxsize else maxsize
            gene_name = request.POST.get("gene_name", "")
            gene_symbol = request.POST.get("gene_symbol", "")
            function = request.POST.get("function", "")
            motif = request.POST.get("motif", "")
            reading_frame = request.POST.get("read_direction", "")
            hits = GeneProtein.objects
            hits = hits.select_related("chromosome")
            hits = hits.select_related("annotation")
            hits = hits.select_related("geneseq")
            hits = (
                hits.filter(chromosome__chromosome__istartswith=chromosome)
                if chromosome
                else hits
            )
            hits = hits.filter(chromosome__specie__icontains=specie) if specie else hits
            hits = hits.filter(chromosome__strain__iexact=strain) if strain else hits
            hits = hits.filter(dna_length__gte=minsize) if minsize else hits
            hits = hits.filter(dna_length__lte=maxsize) if maxsize else hits
            hits = (
                hits.filter(annotation__gene_name__iexact=gene_name)
                if gene_name
                else hits
            )
            hits = (
                hits.filter(annotation__gene_symbol__iexact=gene_symbol)
                if gene_symbol
                else hits
            )
            hits = (
                hits.filter(annotation__function__icontains=function)
                if len(function) >= 3
                else hits
            )
            hits = hits.filter(geneseq__sequence__icontains=motif) if motif else hits
            if reading_frame == "direct":
                hits = hits.filter(reading_frame=1)
            elif reading_frame == "reverse":
                hits = hits.filter(reading_frame=-1)
            context = {"hits": hits} if hits.count() < 100 else {"hits": hits[:100]}
        # Launch a blast request
        elif "database" in request.POST:
            sequence = request.POST["sequence"]
            database = request.POST["database"]
            optimization = False if request.POST["optimization"] == "blastn" else True
            word_size = request.POST["word-size"] if request.POST["word-size"] else 10
            blast_hits = launch_blast(
                sequence=sequence,
                database=database,
                word_size=word_size,
                megablast=optimization,
            )
            context = {"hits": blast_hits}
            return render(request, self.BLAST_template, context)

        return render(request, self.POST_template, context)


class ProteinView(View):
    """Manage Protein's view logic"""

    GET_template = "protein_form.html"
    POST_template = "protein_query.html"
    ENTRY_template = "single_protein_entry.html"

    def get(self, request):
        """Method used to process GET requests"""
        if "protein" in request.GET:
            accession_number = request.GET["protein"]
            entry = get_object_or_404(
                GeneProtein.objects.select_related("chromosome")
                .select_related("annotation")
                .select_related("proteinseq"),
                accession_number=accession_number,
            )
            context = {"entry": entry}
            return render(request, self.ENTRY_template, context)
        else:
            return render(request, self.GET_template, {})

    def post(self, request):
        """Method used to process POST requests"""
        context = {"hits": []}

        if "ac" in request.POST:
            accession_number = request.POST.get("ac", "")
            hits = GeneProtein.objects
            hits = hits.filter(accession_number__istartswith=accession_number)
            hits = hits.select_related("chromosome").select_related("annotation")
            context = {"hits": hits} if hits.count() < 100 else {"hits": hits[:100]}
        elif "chromosome" in request.POST:
            chromosome = request.POST.get("chromosome", "")
            specie = request.POST.get("specie", "")
            strain = request.POST.get("strain", "")
            minsize = request.POST.get("minsize", "")
            maxsize = request.POST.get("maxsize", "")
            minsize = int(minsize) if minsize else minsize
            maxsize = int(maxsize) if maxsize else maxsize
            gene_name = request.POST.get("gene_name", "")
            gene_symbol = request.POST.get("gene_symbol", "")
            function = request.POST.get("function", "")
            motif = request.POST.get("motif", "")
            hits = GeneProtein.objects
            hits = hits.select_related("chromosome")
            hits = hits.select_related("annotation")
            hits = hits.select_related("proteinseq")
            hits = (
                hits.filter(chromosome__chromosome__istartswith=chromosome)
                if chromosome
                else hits
            )
            hits = hits.filter(chromosome__specie__icontains=specie) if specie else hits
            hits = hits.filter(chromosome__strain__iexact=strain) if strain else hits
            hits = hits.filter(dna_length__gte=minsize) if minsize else hits
            hits = hits.filter(dna_length__lte=maxsize) if maxsize else hits
            hits = (
                hits.filter(annotation__gene_name__iexact=gene_name)
                if gene_name
                else hits
            )
            hits = (
                hits.filter(annotation__gene_symbol__iexact=gene_symbol)
                if gene_symbol
                else hits
            )
            hits = (
                hits.filter(annotation__function__icontains=function)
                if len(function) >= 3
                else hits
            )
            hits = hits.filter(proteinseq__sequence__icontains=motif) if motif else hits
            context = {"hits": hits} if hits.count() < 100 else {"hits": hits[:100]}

        return render(request, self.POST_template, context)
