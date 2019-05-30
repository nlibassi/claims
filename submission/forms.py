from django import forms
from .models import InsuredProfile, DependentProfile, Profile, Report, Claim
import datetime

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, datetime.datetime.now().year + 1)), initial = datetime.datetime.now().year - 50)

    class Meta:
        model = Profile
        fields = ['first_name', 'middle_name', 'last_name', 'gender',
                        'date_of_birth', 'residence_country', 'foreign_currency_default', 'other_coverage', 
                        'other_insurance_co', 'other_plan_name', 'other_plan_id', 'medicare_part_a', 
                        'medicare_part_b', 'medicare_id']


class InsuredProfileForm(ProfileForm):

    class Meta:
        model = InsuredProfile
        fields = ['first_name', 'middle_name', 'last_name', 'gender',
                        'date_of_birth', 'email', 'air_id', 'mailing_street', 'mailing_optional', 'mailing_city',
                        'mailing_state', 'mailing_zip', 'residence_country', 'foreign_currency_default', 'other_coverage', 
                        'other_insurance_co', 'other_plan_name', 'other_plan_id', 'medicare_part_a', 
                        'medicare_part_b', 'medicare_id',]
        widgets = {
                'description': forms.Textarea(),
        }

    """
    def save(self, commit=True):
        profile = super(InsuredProfileForm, self).save(commit=commit)
        # not returning anything?
        #item.code.description = self.cleaned_data['description']
        #item.code.save()
    """

class DependentProfileForm(ProfileForm):
    
    class Meta:
        model = DependentProfile
        fields = ['first_name', 'middle_name', 'last_name', 'gender',
                        'date_of_birth', 'relationship_to_insured', 'residence_country',
                        'foreign_currency_default', 'other_coverage', 
                        'other_insurance_co', 'other_plan_name', 'other_plan_id', 'medicare_part_a', 
                        'medicare_part_b', 'medicare_id', 'full_time_student']
        widgets = {
                'description': forms.Textarea(),
        }

    # not sure why choices are not being limited here? seems to be doing nothing
    def __init__(self, *args, **kwargs):
        super(DependentProfileForm,self).__init__(*args,**kwargs)
        choices = (('Spouse', 'Spouse'),
                        ('Child', 'Child'))
        self.fields['relationship_to_insured'].choices = choices


    def save(self, commit=True):
        profile = super(DependentProfileForm, self).save(commit=commit)
        return profile
        #item.code.description = self.cleaned_data['description']
        #item.code.save()


# originally had no ReportForm as Report instance was created upon user selection of patient name
class ReportForm(forms.ModelForm):
    accident_date = forms.DateField(widget=forms.SelectDateWidget(
        years=range(datetime.datetime.now().year - 5, datetime.datetime.now().year + 1)))

    class Meta:
        model = Report
        fields = ['diagnosis', 'employment_related', 'auto_accident_related', 'other_accident_related', 
                        'accident_date', 'accident_details', 'full_time_student', 'school_name']


class ClaimForm(forms.ModelForm):
    service_date = forms.DateField(widget=forms.SelectDateWidget(
        years=range(datetime.datetime.now().year - 5, datetime.datetime.now().year + 1)))

    class Meta:
        model = Claim
        fields = ['claim_type', 'service_date', 'service_description', 'service_place', 
        'foreign_charges', 'foreign_currency', 'receipt_file', 'receipt_image',]
        widgets = {
            'description': forms.Textarea()
        }