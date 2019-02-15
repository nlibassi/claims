#from django.shortcuts import render

#from django.shortcuts import get_object_or_404, render

#from django.http import HttpResponse, HttpResponseRedirect
#from django.views import generic

from django.views.generic import View
from django.utils import timezone
from .models import *
from .render import Render

#from easy_pdf.views import PDFTemplateView

# Create your views here.

class Pdf(View):

    def get(self, request):
        sales = Sales.objects.all()
        today = timezone.now()
        params = {
                'today': today,
                'sales': sales,
                'request': request
        }
        return Render.render('pdf.html', params)
        # no need for HttpResponse here as it is handled by the Render.render method

#def index(request):
    #return HttpResponse("Hey, this is the submission index.")

#class HelloPDFView(PDFTemplateView):
    #template_name = 'hello.html'

#class IndexView(generic.ListView):
    #template_name = 'submission/hello.html'
    #context_object_name = 'latest_question_list'
