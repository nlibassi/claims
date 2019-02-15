from django.shortcuts import render

from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

#from easy_pdf.views import PDFTemplateView

# Create your views here.

def index(request):
    return HttpResponse("Hey, this is the submission index.")

#class HelloPDFView(PDFTemplateView):
    #template_name = 'hello.html'

#class IndexView(generic.ListView):
    #template_name = 'submission/hello.html'
    #context_object_name = 'latest_question_list'
