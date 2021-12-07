"""
Home views
"""
from django.views import View
from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
class HomeView(View):
    """ HomePage Logic """

    POST_template = GET_template = "home.html"

    def get(self, request):
        """Method used to process GET requests"""
        context = {}
        return render(request, self.GET_template, context)

    def post(self, request):
        """Method used to process POST requests"""
        context = {}
        return render(request, self.POST_template, context)
