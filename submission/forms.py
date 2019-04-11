from django import forms
from .models import InsuredProfile, DependentProfile, Profile, Claim

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget)

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
                        'medicare_part_b', 'medicare_id', 'has_dependent']
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

    def save(self, commit=True):
        profile = super(DependentProfileForm, self).save(commit=commit)
        return profile
        #item.code.description = self.cleaned_data['description']
        #item.code.save()


class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        fields = ['diagnosis', 'employment_related', 'auto_accident_related',
        'other_accident_related', 'full_time_student', 'claim_type', 'service_date',
        'service_description', 'service_place', 'foreign_charges', 'foreign_currency']
        widgets = {
            'description': forms.Textarea()
        }