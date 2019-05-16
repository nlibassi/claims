
from django.conf.urls import url, include
from django.views.generic.base import TemplateView

# import as submission_views in case of a separate app in the future - activate later
from . import views

# supposedly the following should work in place of all the individual imports below:
# url('^', include('django.contrib.auth.urls'))
# but have not yet gotten it  working

from django.contrib.auth import views as auth_views
"""
from django.urls import reverse_lazy
from django.contrib.auth.views import(
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)
"""
#   url(r'^signup/$', submission_views.signup, name='signup'),
#   url(r'^$', views.index, name='index')
#   url(r'^signup/$', views.signup, name='signup'),

#   url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
#   url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout')


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.SignUp.as_view(), name='register'),
    #url(r'^update_profile/$', views.update_profile_form, name='update_profile_form'),
    #url(r'^complete_profile/(?P<username>[\w.@+-]+)/$', views.InsuredProfileUpdateView.as_view(template_name='insuredprofile_form.html'), name='complete_profile_form'),
    
    # completing insured profile is same as updating as insured profile is created at user creation
    #url(r'^complete_profile/(?P<pk>\d+)/$', views.InsuredProfileUpdateView.as_view(template_name='insuredprofile_form.html'), name='complete_profile_form'),
    #url(r'^complete_profile/(?P<user>\w+)/$', views.InsuredProfileCreateView.as_view(template_name='insuredprofile_form.html'), name='complete_insured_profile_form'),
    #url(r'^$', views.InsuredProfileCreateView.as_view(template_name='insuredprofile_form.html'), name='complete_insured_profile_form'),
    url(r'^complete_dependent_profile/$', views.DependentProfileCreateView.as_view(template_name='dependentprofile_form.html'), name='complete_dependent_profile_form'),
    #pk here is for insuredprofile not for user
    #url(r'^update_profile/(?P<username>[\w.@+-]+)/$', views.InsuredProfileUpdateView.as_view(template_name='insuredprofile_form.html'), name='update_profile_form'),
    url(r'^update_profile/(?P<pk>\d+)/$', views.InsuredProfileUpdateView.as_view(template_name='insuredprofile_form.html'), name='update_profile_form'),
    url(r'^profile_updated/$', views.InsuredProfileUpdated.as_view(template_name='profile_updated.html'), name='profile_updated'),
    url(r'^dependent_profile_complete/$', views.DependentProfileCompleteView.as_view(template_name='dependent_profile_complete.html'), name='dependent_profile_complete'),
    url(r'^update_dependent_profile/(?P<pk>\d+)/$', views.DependentProfileUpdateView.as_view(template_name='dependentprofile_form_update.html'), name='update_dependent_profile'),
    url(r'^dependent_profile_updated/$', views.DependentProfileUpdated.as_view(), name='dependent_profile_updated'),
    url(r'^complete_claim_form/(?P<profile_slug>[-\w]+)/$', views.ClaimCreateView.as_view(template_name='claim_form.html'), name='complete_claim_form'),
    #url(r'^(?P<first_name>\w+)/$', views.DependentProfileUpdateView.as_view(template_name='dependentprofile_form.html'), name='update_dependent_profile'),
    #url(r'^file_claim_report/$', TemplateView.as_view(template_name='file_claim_report.html'), name='file_claim_report'),
    url(r'^report_created/(?P<profile_slug>[-\w]+)/$', views.ReportCreatedView.as_view(template_name='report_created.html'), name='report_created'),
    url(r'^claim_list/(?P<profile_slug>[-\w]+)/$', views.ClaimListView.as_view(template_name='claim_list.html'), name='claim_list'),
    #url(r'^delete_claim/$', views.delete_claim, name='delete_claim'),
    url(r'^update_claim/(?P<pk>\d+)/$', views.ClaimUpdateView.as_view(), name='update_claim'),
    url(r'^delete_claim/(?P<pk>\d+)/$', views.ClaimDeleteView.as_view(), name='delete_claim'),
    url(r'^report_details/(?P<profile_slug>[-\w]+)/$', views.DisplayPdf.as_view(template_name='pdf.html'), name='display_report'),
    #url(r'^submit_report/(?P<profile_slug>[-\w]+)/$', views.SubmitPdf.as_view(template_name='report_submitted.html'), name='submit_report'),
    url(r'^report_submitted/(?P<profile_slug>[-\w]+)/$', views.ReportSubmittedView.as_view(template_name='report_submitted.html'), name='report_submitted'),
    url(r'^$', views.Welcome.as_view(template_name='welcome.html'), name='welcome'),
    ]

# may try to add username to url as below
#url(r'(?P<username>)/welcome/$', TemplateView.as_view(template_name='welcome.html'), name='welcome')
#url(r'^profile_complete/$', views.insured_profile_complete, name='profile_complete'),
#url(r'^create_insured_profile/$', views.InsuredProfileCreate.as_view(), name='create_insured_profile')
#url(r'^profile_complete/$', views.insured_profile_complete, name='profile_complete'),