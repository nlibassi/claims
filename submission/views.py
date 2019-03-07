#from django.shortcuts import render

#from django.shortcuts import get_object_or_404, render

#from django.http import HttpResponse, HttpResponseRedirect
#from django.views import generic

from django.views import generic
from django.views.generic import View
from django.utils import timezone
from .models import *
from .render import Render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .models import InsuredProfile 

from django.shortcuts import redirect


#from easy_pdf.views import PDFTemplateView

# Create your views here.

# is CreateView in django.views.generic or django.views.generic.edit?
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Welcome(generic.TemplateView):
    #success_url = reverse_lazy('welcome')
    #template_name = 'welcome.html'
    def get(self, request):
        params = {'request': request}
        return Render.render('welcome.html', params)


class InsuredProfileCreate(generic.CreateView):
    model = InsuredProfile
    success_url = '/profile_complete'
    fields = ['email', 'first_name', 'middle_name', 'last_name', 'gender',
                    'date_of_birth', 'air_id', 'mailing_street', 'mailing_optional', 'mailing_city',
                    'mailing_state', 'mailing_zip', 'mailing_country', 'residence_country',
                    'foreign_currency_default', 'other_coverage', 'other_insurance_co',
                    'other_plan_name', 'other_plan_id', 'medicare_part_a', 'medicare_part_b',
                    'medicare_id', 'full_time_student', 'has_dependent']
    # no need to give a template OR forms.py in this situation? 
    # form and template auto-created?
    #template_name = 'whatever.html'
    # function needed for saving info or only in template?


class InsuredProfileComplete(generic.TemplateView):

    def get(self, request):
        params = {'request': request}
        return Render.render('profile_complete.html', params)




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
