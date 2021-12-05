"""
Docstring
"""
from django.views import View
from django.shortcuts import render

from annotation.models import Genome


def something(request):
    pass


# Create your views here.
class GenomeView(View):
    """Manage logic to the genome view"""

    GET_template = "genome_form.html"

    def get(self, request):
        """Method used to process GET requests"""
        # The dict's keys should be valid Python identifiers :
        # a combination of numbers, letters, and underscores, starting with a letter
        context = {"name": "value", "x": 5, "y": 17}
        return render(request, self.GET_template, context)

    def post(self, request):
        """Method used to process POST requests"""
        pass
