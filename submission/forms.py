from django import forms
from .models import InsuredProfile


class InsuredProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget)

    

    class Meta:
        model = InsuredProfile
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'gender',
                    'date_of_birth', 'air_id', 'mailing_street', 'mailing_optional', 'mailing_city',
                    'mailing_state', 'mailing_zip', 'residence_country',
                    'foreign_currency_default', 'other_coverage', 'other_insurance_co',
                    'other_plan_name', 'other_plan_id', 'medicare_part_a', 'medicare_part_b',
                    'medicare_id', 'full_time_student', 'has_dependent']
        widgets = {
                'description': forms.Textarea(),
        }