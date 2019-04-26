#from django.shortcuts import render

#from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
#from django.views import generic

from django.views import generic
from django.views.generic import View, CreateView, UpdateView, TemplateView, DetailView, ListView
from django.utils import timezone
# add other models by name later
from .models import InsuredProfile, DependentProfile, Report, Claim
from .forms import InsuredProfileForm, DependentProfileForm, ClaimForm
from .render import Render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.urls import reverse_lazy

from django.shortcuts import redirect, get_object_or_404, render

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.http import require_http_methods

from django.forms import ModelForm

from django.core.exceptions import ValidationError


#from easy_pdf.views import PDFTemplateView

def profile_slug_to_first_last_name(profile_slug):
    """
    convert profile slug to first and last name in title case
    arg: profile slug as string e.g. 'bob-smith'
    ret: title case version of name as string e.g. 'Bob Smith'
    """
    name_list = profile_slug.split('-')
    name_list = [name.title() for name in name_list]
    name_first_last_title = ' '.join(name_list)
    return name_first_last_title

def validate_single_open_report(request, profile_slug):
    """
    validates that only one instance of an unsubmitted report exists per person
    """

    patient_reports = Report.objects.filter(patient_slug=profile_slug)
    name_first_last_title = profile_slug_to_first_last_name(profile_slug)
    if patient_reports:
        if not any([report.submitted for report in patient_reports]):
            messages.error(request, "Please first submit open report for {}.".format(name_first_last_title))
            #raise ValidationError("Please first submit open report for {}.".format(name_first_last_title))
    else:
        return True


# Create your views here.

# is CreateView in django.views.generic or django.views.generic.edit?
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    """
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        #user.save()
        InsuredProfile.objects.create(user=user)
        return HttpResponse('User registered')
    """
class Welcome(TemplateView):
    #success_url = reverse_lazy('welcome')
    template_name = 'welcome.html'

    # get() method not required with TemplateView
    """
    def get(self, request):
        params = {'request': request}
        return Render.render('welcome.html', params)
    """

# add login_required decorator to class or function

class InsuredProfileCreateView(CreateView):
    form_class = InsuredProfileForm
    # if template name is given in urls shouldn't be necessary here
    template_name = 'insuredprofile_form.html'
    # may not need to define model here as it is defined in InsuredProfileForm
    model = InsuredProfile
    success_url = reverse_lazy('profile_updated')

    
    # is this necessary? yes, overriding default form_valid() method so profile gets
    # saved under current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()  # This is redundant, see comments. ??
        return super(InsuredProfileCreateView, self).form_valid(form)

    """
    def get_success_url(self, request):
        #pk = request.user.pk
        return reverse_lazy('profile_updated', kwargs={'pk': request.session['user_id']})
        #return reverse_lazy('profile_updated', kwargs={'pk': pk})
    """

class InsuredProfileUpdateView(UpdateView):
    form_class = InsuredProfileForm
    # may not need to define model here as it is defined in InsuredProfileForm
    model = InsuredProfile
    success_url = reverse_lazy('profile_updated')

    def form_valid(self, form):
        form.instance.user = self.request.user
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()  # This is redundant, see comments. ??
        return super(InsuredProfileUpdateView, self).form_valid(form)

    """
    def get_success_url(self, request):
        #pk = request.user.pk
        return reverse_lazy('profile_updated', kwargs={'pk': request.session['user_id']})
        #return reverse_lazy('profile_updated', kwargs={'pk': pk})
    """

class DependentProfileCreateView(CreateView):
    form_class = DependentProfileForm
    template_name = 'dependentform_profile.html'
    success_url = reverse_lazy('dependent_profile_complete')

    #def form_invalid(self, form):
        #return http.HttpResponse("form is invalid.. this is just an HttpResponse object")

    def form_valid(self, form):
        #form.instance.insured = self.request.user
        profile = form.save(commit=False)
        profile.insured = self.request.user
        profile.save()  # This is redundant, see comments. ??
        return super(DependentProfileCreateView, self).form_valid(form)

# not using
class DependentProfileCompleteView(TemplateView):
    template_name = 'dependent_profile_complete.html'
    

class DependentProfileUpdateView(UpdateView):
    form_class = DependentProfileForm
    model = DependentProfile

    #def get_queryset(self, request):
        #return super().get_queryset().filter(board=self.kwargs['board_id'])

    def get_success_url(self, request):
        #pk = request.user.pk
        return reverse_lazy('dependent_profile_updated', kwargs={'pk': request.session['user_id']})
        #return reverse_lazy('profile_updated', kwargs={'pk': pk})


# turn this into CreateReportView - separate view where patient is chosen (single-field form?)
class ReportCreatedView(View):
    print('ReportCreatedView available')
    model = Report
    template_name = 'report_created.html'
    #http_method_names = ['get', 'post']
    
    # probably shouldn't be creating report in get() method but trying to 
    # minimize user's clicks
    def get(self, request, profile_slug):
        insured_profile = request.user.insuredprofile
        if validate_single_open_report(request, profile_slug):
            report = Report.objects.create(insured_profile=insured_profile)
            if profile_slug != request.user.insuredprofile.profile_slug:
                dependent_profiles = request.user.dependents.all()
                for dependent_profile in dependent_profiles:
                    if dependent_profile.profile_slug == profile_slug:
                        report.patient_slug = dependent_profile.profile_slug
            else:
                report.patient_slug = profile_slug
            report.save()
            patient_first_last_name = profile_slug_to_first_last_name(profile_slug)
            context = {'patient_first_last_name': patient_first_last_name, 'profile_slug': profile_slug}
            return render(request, self.template_name, context)
        else:
            return render(request, 'error.html')
            # can I render a different view here if validation fails?
 

    # trash
    """
    def get(self, request):
        insured_profile = request.user.insuredprofile
        if request.user.first_name in request:
            report = Report.objects.create(insured_profile=insured_profile)
        elif request.user.first_name not in request:
            for dependent in request.user.dependents.all:
                if dependent.first_name in request:
                    dependent_profile = dependent.dependentprofile
                    report = Report.objects.create(insured_profile=insured_profile, dependent_profile=dependent_profile)
        else:
            print('no report created')
        report.save()
        return super(ReportCreatedView, self)
    """
        

    # from example
    """
    def get_context_data(self, **kwargs):
        context = super(ReportCreatedView, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context
    """


class ClaimCreateView(CreateView):
    form_class = ClaimForm
    template_name = 'claim_form.html'
    success_url = reverse_lazy('claim_list')

    # trying to pre-populate the form with this - should this be done in the form itself instead?
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        form.foreign_currency = request.user.insuredprofile.foreign_currency_default
        return render(request, self.template_name, {'form': form})
        #return render(request, self.template_name, {'form': form, 'profile_slug': profile_slug})

    # finish writing this
    def form_valid(self, form):
        form.instance.user = self.request.user
        claim = form.save(commit=False)
        claim.insured_profile = self.request.user.insuredprofile
        # dependent_profile should come from form used to create report
        #claim.dependent_profile = self.request. # what?
        claim.save()  # This is redundant, see comments. ??
        return super(ClaimCreateView, self).form_valid(form)

    #success_url = reverse_lazy()


class ClaimListView(ListView):
    model = Claim
    template_name = 'claim_list.html'

    def get(self, request, profile_slug, *args, **kwargs):
        return render(request, self.template_name, {'profile_slug': profile_slug})

    def get_queryset(self, profile_slug):
        return Claim.objects.filter(report__patient_slug=profile_slug).filter(report__submitted=False)
"""
class UpdateProfileForm(View):
    form_class = InsuredProfileForm
    template_name = 'insuredprofile_form.html'

    # Handle GET HTTP requests
    def get(self, request, *args, **kwargs):
        print('get request received')
        #form = self.form_class(initial=self.initial)
        if request.user.insuredprofile.profile_complete:
            profile = request.user.insuredprofile
            form = self.form_class(request.GET, instance=profile)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # Handle POST HTTP requests
    def post(self, request, *args, **kwargs):
        print('post request received')
        try:
            profile = request.user.insuredprofile
        except InsuredProfile.DoesNotExist:
            profile = InsuredProfile(user=request.user)
        form = InsuredProfileForm(request.POST, instance=profile)
        #form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            #instance = form.save(commit=False)
            #instance.user = request.user
            #instance.save()
            return HttpResponseRedirect('/profile_updated/')

        return render(request, self.template_name, {'form': form})

def bound_form(request, id): 
    profile = get_object_or_404(InsuredProfile, id=id)
    form = InsuredProfileForm(instance=profile) 
    return render_to_response('insuredprofile_form.html', {'form': form}) 
"""
# partially working FBV 3/21 (post not allowed)
"""
def update_profile_form(request):
    try:
        instance = request.user.insuredprofile
    except InsuredProfile.DoesNotExist:
        instance = InsuredProfile(user=request.user)

    instance = get_object_or_404(InsuredProfile, user=request.user)
    if request.method == 'POST':
        print('post request received')
        form = InsuredProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            print('form is valid')
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
    else:
        print('non-post request received')
        form = InsuredProfileForm(instance=instance)
    context = {
       "form": form,
       "instance": instance,}
    return render(request, "insuredprofile_form.html", context)
"""
"""
class InsuredProfileCreate(LoginRequiredMixin, generic.CreateView):
    #login_url = '/login/'
    #model = InsuredProfile
    print('console test - InsuredProfileCreate recognized')
    # form is displayed without template_name being defined
    template_name = 'insuredprofile_form.html'
    http_method_names = ['get', 'post']
    form_class = InsuredProfileForm
    success_url = reverse_lazy('profile_complete')

    def form_valid(self,form):
        super(InsuredProfileCreate, self).form_valid(form)
        # Add action to valid form phase
        messages.success(self.request, 'Profile created successfully!')        
        return HttpResponseRedirect(self.get_success_url())        
    def form_invalid(self,form):
        # Add action to invalid form phase
        messages.info(self.request, 'Profile not created')
        return self.render_to_response(self.get_context_data(form=form))
"""

class InsuredProfileUpdated(generic.TemplateView):
    print('console test - InsuredProfileUpdated recognized')
    template_name = 'profile_updated.html'
    #http_method_names = ['get']

    """
    def get_context_data(self, *args, **kwargs):
        context = super(InsuredProfileComplete.self).get_context_data(*args, **kwargs)
        context['message'] = 'Testing'
        return context
    """
    #http_method_names = ['get', 'post']
"""
class InsuredProfileComplete(View):
    def post(self, request):
        params = {'request': request}
        return Render.render('profile_complete.html', params)
 
    #def post(self, request, *args, **kwargs):
"""


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
