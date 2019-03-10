
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

# 

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    
    url(r'^signup/$', views.SignUp.as_view(), name='register'),
    url(r'^create_insured_profile/$', views.InsuredProfileCreate.as_view(), name='create_insured_profile'),
    url(r'', TemplateView.as_view(template_name='welcome.html'), name='welcome'),
    url(r'^profile_complete/$', TemplateView.as_view(template_name='profile_complete.html'), name='profile_complete'),
    url(r'^file_claim_report/$', TemplateView.as_view(template_name='file_claim_report.html'), name='file_claim_report'),
    ]

# may try to add username to url as below
#url(r'(?P<username>)/welcome/$', TemplateView.as_view(template_name='welcome.html'), name='welcome')


#url(r'^profile_complete/$', views.insured_profile_complete, name='profile_complete'),