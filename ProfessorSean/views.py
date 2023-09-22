from django.http import HttpResponse
from django.views.generic import TemplateView


class Home_Page(TemplateView):
    template_name = "index.html"
