#from django.shortcuts import render

#from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
#from django.views import generic

from django.views import generic
# arent' some of these in generic.edit?
from django.views.generic import View, TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
# add other models by name later
from .models import InsuredProfile, DependentProfile, Report, Claim, Sales
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

from threading import Thread, activeCount

from django.core.mail import send_mail, EmailMessage


# helper functions

def profile_slug_to_first_last_name(profile_slug):
    """
    convert profile slug to first and last name in title case
    arg: profile slug as string e.g. 'bob-smith'
    ret: title case version of name as string e.g. 'Bob Smith'
    """
    name_list = profile_slug.split('-')
    name_list = [name.title() for name in name_list]
    first_last_name_title = ' '.join(name_list)
    return first_last_name_title


def profile_slug_to_first_name(profile_slug):
    """
    convert profile slug to first name in title case
    arg: profile slug as string e.g. 'bob-smith'
    ret: title case version of name as string e.g. 'Bob'
    """
    first_name = profile_slug.split('-')[0]
    first_name_title = first_name.title()
    return first_name_title


def first_last_name_to_profile_slug(first_name, last_name):
    return first_name.lower() + '-' + last_name.lower()


def validate_single_open_report(request, profile_slug):
    """
    validates that only one instance of an unsubmitted report exists per person
    """

    patient_reports = Report.objects.filter(patient_slug=profile_slug)
    name_first_last_title = profile_slug_to_first_last_name(profile_slug)
    if patient_reports:
        if any([report.submitted == False for report in patient_reports]):
            messages.error(request, "Please first submit open report for {}.".format(name_first_last_title))
            #raise ValidationError("Please first submit open report for {}.".format(name_first_last_title))
        else:
            return True

# Views - FBVs

"""
# not using DeleteView CBV as no need to show a confirmation view/template after deletion
def delete_claim(request, pk):
    claim = Claim.objects.get(pk=pk) #get_object_or_404(Claim, pk=pk)
    claim.delete()
    # would prefer to return to 'claim_list' here - use redirect?
    return HttpResponseRedirect('claim_list')
    #return reverse_lazy('delete_claim')
"""

# Views - CBVs

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

    def post(self, request, *args, **kwargs):
        user_reports = self.request.user.insuredprofile.reports.all()
        open_user_reports = user_reports.filter(submitted=False)
        open_user_reports_patient_slugs = [open_user_report.patient_slug for open_user_report in open_user_reports]
        open_user_reports_first_names = [profile_slug_to_first_name(open_user_reports_patient_slug) \
                                                             for open_user_reports_patient_slug in open_user_reports_patient_slugs]
        context = {'open_user_reports_patient_slugs': open_user_reports_patient_slugs,
                            'open_user_reports_first_names' : open_user_reports_first_names
                        }
        return render(request, self.template_name, context=context)

    # get() method not required with TemplateView
    """
    def get(self, request):
        params = {'request': request}
        return Render.render('welcome.html', params)
    """

# add login_required decorator to class or function

# no InsuredProfileCreateView anymore as it is created upon user creation and updated thereafter

class InsuredProfileUpdateView(UpdateView):
    form_class = InsuredProfileForm
    # may not need to define model here as it is defined in InsuredProfileForm
    model = InsuredProfile
    success_url = reverse_lazy('profile_updated')

    def form_valid(self, form):
        form.instance.user = self.request.user
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.save()
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
        user_dependents = self.request.user.dependents.all()
        form_name_slug_form = first_last_name_to_profile_slug(profile.first_name, profile.last_name)
        if user_dependents.filter(profile_slug=form_name_slug_form).exists():
            raise ValidationError("Dependent profile already exists.")
        profile.save()
        return super(DependentProfileCreateView, self).form_valid(form)


class DependentProfileCompleteView(TemplateView):
    template_name = 'dependent_profile_complete.html'

    def get(self, request, *args, **kwargs):
        # get user's dependents, then get newest dependent?
        insureds_newest_dependent_profile = self.request.user.dependents.filter().order_by('-created')[0]
        insureds_newest_dependent_first_name = insureds_newest_dependent_profile.first_name
        # look at admin_order_field attribute - requires adding method to Model class then setting with
        # method_name.admin_order_field
        return render(request, self.template_name, context={'insureds_newest_dependent_first_name' : insureds_newest_dependent_first_name})
    

class DependentProfileUpdateView(UpdateView):
    form_class = DependentProfileForm
    model = DependentProfile
    # template name is defined in url - this is probably unnecessary
    template_name = 'dependentform_profile_update.html'

    #def get_queryset(self, request):
        #return super().get_queryset().filter(board=self.kwargs['board_id'])

    def get_context_data(self, **kwargs):
        dependent_profile_pk = self.kwargs['pk']
        context = {'dependent_profile_pk': dependent_profile_pk}
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        dependent_profile = DependentProfile.objects.get(pk=context['dependent_profile_pk'])
        form = self.form_class(instance=dependent_profile)
        context['form'] = form
        return render(request, self.template_name, context)


    def form_valid(self, form):
        #form.instance.insured = self.request.user
        profile = form.save(commit=False)
        profile.save()
        return super(DependentProfileUpdateView, self).form_valid(form)


    def get_success_url(self):
        #pk = request.user.pk
        #return reverse_lazy('dependent_profile_updated', kwargs={'pk': request.session['user_id']})
        return reverse_lazy('dependent_profile_updated')


# turn this into CreateReportView - separate view where patient is chosen (single-field form?)
class ReportCreatedView(View):
    model = Report
    template_name = 'report_created.html'
    #http_method_names = ['get', 'post']
    
    # probably shouldn't be creating report in get() method but trying to 
    # minimize user's clicks - but maybe should move report attribute population to post()
    def get(self, request, profile_slug):
        insured_profile = request.user.insuredprofile
        if validate_single_open_report(request, profile_slug):
            report = Report.objects.create(insured_profile=insured_profile)
            if profile_slug != request.user.insuredprofile.profile_slug:
                dependent_profiles = request.user.dependents.all()
                for dependent_profile in dependent_profiles:
                    if dependent_profile.profile_slug == profile_slug:
                        report.dependent_profile = dependent_profile
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
 

class ClaimCreateView(CreateView):
    form_class = ClaimForm
    template_name = 'complete_claim_form'
    #context = get_context_data(self)
    #success_url = reverse_lazy('claim_list', kwargs={'profile_slug': profile_slug})

    def get_success_url(self, **kwargs):
        #context = get_context_data()
        profile_slug = self.kwargs['profile_slug']
        return reverse_lazy('claim_list', kwargs={'profile_slug': profile_slug})
    
    
    def get(self, request, profile_slug, *args, **kwargs):
        #form = self.form_class(initial=self.initial)
        if profile_slug != self.request.user.insuredprofile.profile_slug:
            report = Report.objects.filter(submitted=False).get(patient_slug=profile_slug)
            dependent_profile = report.dependent_profile
            form = self.form_class(initial={'foreign_currency': request.user.insuredprofile.foreign_currency_default,
                                                        'full_time_student': dependent_profile.full_time_student})
        else:
            form = self.form_class(initial={'foreign_currency': request.user.insuredprofile.foreign_currency_default})
        #return render(request, self.template_name, {'form': form})
        patient_first_last_name = profile_slug_to_first_last_name(profile_slug)
        return render(request, self.template_name, {'form': form, 'profile_slug': profile_slug, 'patient_first_last_name': patient_first_last_name})


    def get_context_data(self, *args, **kwargs):
        #context = super(ClaimCreateView, self).get_context_data(*args, **kwargs)
        profile_slug = self.kwargs['profile_slug']
        patient_first_last_name = profile_slug_to_first_last_name(profile_slug)
        context = {'profile_slug': profile_slug, 'patient_first_last_name': patient_first_last_name}
        return context


    # profile_slug cannot be passed as arg here
    # The form_valid() method for CreateView and UpdateView saves the form, then redirects to the success url. 
    def form_valid(self, form):
        form.instance.user = self.request.user
        claim = form.save(commit=False)
        claim.insured_profile = self.request.user.insuredprofile
        context = self.get_context_data()
        claim.report = Report.objects.filter(patient_slug=context['profile_slug']).get(submitted=False)
        # still may need to avoid defining profiles on both report and claims but doing this for now
        claim.dependent_profile = claim.report.dependent_profile
        if claim.receipt_file or claim.receipt_image:
            claim.save()
        else:
            messages.error(self.request, "Please first add receipt to claim.")
        return super(ClaimCreateView, self).form_valid(form)

    # cannot pass profile_slug to get_success_url() in this way
    #def get_success_url(self, *args, **kwargs):
        #return reverse_lazy('claim_list/' + self.request.profile_slug + '/')

    
    #success_url = reverse_lazy()


class ClaimListView(ListView):
    model = Claim
    template_name = 'claim_list'

    """
    def get_context_data(self, **kwargs):
        context = super(ClaimListView, self).get_context_data(**kwargs)
        #claims = Claim.objects.filter(report__patient_slug=profile_slug).filter(report__submitted=False)
        claims1 = Claim.objects.filter(report__submitted=False)
        context.update({'claims1': claims1})
        return context
    """

    def get(self, request, *args, **kwargs):
        profile_slug = self.kwargs['profile_slug']
        report_first_last_name = profile_slug_to_first_last_name(profile_slug)
        report = Report.objects.filter(patient_slug=profile_slug).filter(submitted=False)
        report_claims = Claim.objects.filter(report=report)
        context = {'profile_slug': profile_slug, 
                            'report_first_last_name': report_first_last_name, 
                            'report_claims': report_claims}
        return render(request, self.template_name, context=context)

    #def get_queryset(self, profile_slug):
        #return Claim.objects.filter(report__patient_slug=profile_slug).filter(report__submitted=False)

class ClaimUpdateView(UpdateView):
    form_class = ClaimForm
    model = Claim
    template_name = 'claim_form_update.html'

    
    def get_context_data(self, **kwargs):
        claim_pk = self.kwargs['pk']
        claim = Claim.objects.get(pk=claim_pk)
        profile_slug = claim.report.patient_slug
        patient_first_last_name = profile_slug_to_first_last_name(profile_slug)
        context = {'claim_pk': claim_pk, 'patient_first_last_name': patient_first_last_name, 'profile_slug': profile_slug}
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        claim = Claim.objects.get(pk=context['claim_pk'])
        form = self.form_class(instance=claim)
        context['form'] = form
        return render(request, self.template_name, context)


    def form_valid(self, form):
        claim = form.save(commit=False)
        claim.save()
        return super(ClaimUpdateView, self).form_valid(form)


    def get_success_url(self):
        profile_slug = self.get_context_data()['profile_slug']
        return reverse_lazy('claim_list', kwargs={'profile_slug': profile_slug})


class ClaimDeleteView(DeleteView):
    model = Claim
    #success_url = reverse_lazy('claim_list')

    template_name = 'delete_claim.html'

    def get_success_url(self, **kwargs):
        claim_pk = self.kwargs['pk']
        claim = Claim.objects.get(pk=claim_pk)
        profile_slug = claim.report.patient_slug
        #profile_slug = self.request.pk.report.patient_slug
        #profile_slug = self.kwargs['profile_slug']
        return reverse_lazy('claim_list', kwargs={'profile_slug': profile_slug})

    # cannot have url with pk as once object is deleted pk no longer exists
    """
    def get_success_url(self, **kwargs):
        claim_pk = self.kwargs['pk']
        return reverse_lazy('claim_deleted', kwargs={'pk': claim_pk})
    """

        #return Claim.objects.filter(report__patient_slug=profile_slug)


class InsuredProfileUpdated(TemplateView):
    template_name = 'profile_updated.html'
    #http_method_names = ['get']


class DependentProfileUpdated(TemplateView):
    template_name = 'dependent_profile_updated.html'


class DisplayPdf(View):
    template_name = 'pdf.html'

    def get(self, request, *args, **kwargs):
        #sales = Sales.objects.all()
        profile_slug = self.kwargs['profile_slug']
        report = Report.objects.filter(submitted=False).get(patient_slug=profile_slug)
        claims = Claim.objects.filter(report=report)
        report_first_last_name = profile_slug_to_first_last_name(profile_slug)
        today = timezone.now()
        claims_usd_list = [claim.usd_charges for claim in claims]
        total_claims_usd = sum(claims_usd_list)

        insured_profile = report.insured_profile
        if  report.dependent_profile:
            patient_profile = report.dependent_profile
        else:
            patient_profile = insured_profile
        params = {
                'patient_name': report_first_last_name,
                'today': today,
                'report': report,
                'claims': claims,
                'insured_profile': insured_profile,
                'patient_profile': patient_profile,
                'total_claims_usd': total_claims_usd,
                'request': request,
        }
        return Render.render('pdf.html', params)


# remove repeated code from DisplayPdf (use decorator?)
class ReportSubmittedView(View):
    template_name = 'report_submitted.html'

    def get(self, request, *args, **kwargs):
        #sales = Sales.objects.all()
        profile_slug = self.kwargs['profile_slug']
        report = Report.objects.filter(submitted=False).get(patient_slug=profile_slug)
        claims = Claim.objects.filter(report=report)
        report_first_last_name = profile_slug_to_first_last_name(profile_slug)
        today = timezone.now()
        claims_usd_list = [claim.usd_charges for claim in claims]
        total_claims_usd = sum(claims_usd_list)

        insured_profile = report.insured_profile
        if  report.dependent_profile:
            patient_profile = report.dependent_profile
        else:
            patient_profile = insured_profile
        params = {
                'patient_name': report_first_last_name,
                'today': today,
                'report': report,
                'claims': claims,
                'insured_profile': insured_profile,
                'patient_profile': patient_profile,
                'total_claims_usd': total_claims_usd,
                'request': request,
        }
        report_file = Render.render_to_file('pdf.html', params)
        subject = 'Claim Report'
        text = 'Please find the attached claim report.'
        # test email addresses
        from_email = ['nlibassi@gmail.com']
        to_email = ['nickl@hush.com']

        email = EmailMessage(subject, text, from_email, to_email,)
        #try:
        email.attach_file(report_file)

        # attach receipts to email
        receipt_image_urls = [claim.receipt_image.url for claim in claims if claim.receipt_image]
        receipt_file_urls = [claim.receipt_file.url for claim in claims if claim.receipt_file]
        receipt_urls = receipt_image_urls + receipt_file_urls
        for receipt_url in receipt_urls:
            email.attach_file(receipt_url)
        #except:
            #return "Attachment erorr"
        email.send()
        report.submitted = True
        report.save()
        return render(request, 'report_submitted.html', {'profile_slug': profile_slug, 'report_first_last_name': report_first_last_name})

        # use threading after test
        #thread = Thread(target=email.send())
        #thread.start()


#class ReportSubmitted(TemplateView):
    #template_name = 'report_submitted.html'