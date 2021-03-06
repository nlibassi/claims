from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.urls import reverse
from django import forms
#from django.contrib.auth import get_user_model

from .geography_lists import us_states, countries, currencies

from datetime import datetime
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

from django.template.defaultfilters import slugify

from django.core.exceptions import ValidationError

from forex_python.converter import CurrencyRates

import os
# Create your models here.


# either do this or what was done below
"""
class User(AbstractUser):
    username = models.CharField(blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        return "{}".format(self.email)
"""

GENDER_CHOICES = (
('M', 'Male'),
('F', 'Female')
)
AFFIRM_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No')
    )
US_STATE_CHOICES = tuple(us_states)
COUNTRY_CHOICES = tuple(countries)
CURRENCY_CHOICES = tuple(currencies)


# fields shared by both InsuredProfile and DependentProfile
class Profile(models.Model):
    RELATIONSHIP_CHOICES = (
                                            ('Spouse', 'Spouse'),
                                            ('Child', 'Child'),
                                            ('Self', 'Self')
                                            )
    DEPENDENT_RELATIONSHIP_CHOICES = (
                                            ('Spouse', 'Spouse'),
                                            ('Child', 'Child'),
                                            )
    # this field may need to be taken care of in save() method
    last_modified = models.DateTimeField(default=datetime.utcnow)
    first_name = models.CharField('First Name', max_length=64)
    middle_name = models.CharField('Middle Name', max_length=64)
    last_name = models.CharField('Last Name', max_length=64)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES)
    relationship_to_insured = models.CharField('Relationship to insured', max_length=6, choices=RELATIONSHIP_CHOICES)
    date_of_birth = models.DateField('Date of Birth', null=True)
    residence_country = models.CharField('Residence - Country', max_length=64, choices=COUNTRY_CHOICES, null=True)
    foreign_currency_default = models.CharField('Foreign Currency Default', max_length=64, choices=CURRENCY_CHOICES, null=True)
    other_coverage = models.CharField('Other health insurance coverage?', max_length=1, choices=AFFIRM_CHOICES, null=True)
    other_insurance_co = models.CharField('Other health insurance provider', max_length=64, null=True, blank=True)
    other_plan_name = models.CharField('Other health plan name', max_length=64, null=True, blank=True)
    other_plan_id = models.CharField('Other health plan id', max_length=64, null=True, blank=True)
    medicare_part_a = models.CharField('Medicare Part A coverage?', max_length=1, choices=AFFIRM_CHOICES, null=True)
    medicare_part_b = models.CharField('Medicare Part B coverage?', max_length=1, choices=AFFIRM_CHOICES, null=True)
    medicare_id = models.CharField('Medicare ID', max_length=64, null=True, blank=True)
    profile_slug = models.SlugField()

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __repr__(self):
       return (f'{self.__class__.__name__}('
                    f'{self.first_name!r} {self.last_name!r})')

    def save(self, *args, **kwargs):
        self.profile_slug = slugify(self.first_name + ' ' + self.last_name)
        super(Profile, self).save(*args, **kwargs)


# copied from Flask app - modify for Django, blank=True
class InsuredProfile(Profile):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #base_profile = models.OneToOneField(Profile, on_delete=None)
    # email may also be taken from User if requested at sign up
    email = models.EmailField(max_length=120)
    #password_hash = models.CharField(max_length=128)
    # may also be taken from User?
    air_id = models.CharField('AIR ID', max_length=20, null=True, unique=True)
    mailing_street = models.CharField('Mailing - Street', max_length=64, null=True)
    mailing_optional = models.CharField('Mailing - Optional', max_length=64, null=True, blank=True)
    mailing_city = models.CharField('Mailing - City', max_length=64, null=True)
    mailing_state = models.CharField('Mailing - State', max_length=32, choices=US_STATE_CHOICES, null=True)
    mailing_zip = models.CharField('Mailing - Zip', max_length=10, null=True)
    #mailing_country = models.CharField('Mailing - Country', max_length=64, choices=COUNTRY_CHOICES, null=True)
    # this field may or may not be necessary
    #has_dependent = models.CharField('Does insured have dependents?', max_length=3, choices=AFFIRM_CHOICES)

    # not sure if this method should stay - may not matter as using try/except when completing/updating profile

    class Meta:
        verbose_name = 'Insured Profile'
        verbose_name_plural = 'Insured Profiles'

    def __repr__(self):
       return (f'{self.__class__.__name__}('
                    f'{self.user!r})')
    

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            insured_profile = InsuredProfile(user=user)
            insured_profile.relationship_to_insured = 'Self'
            insured_profile.save()
        
    # why isn't this given as self.create_profile() here? connect expects only a method name, not call?
    post_save.connect(create_profile, sender=User)


    @property
    def profile_complete(self):
        required_fields = [self.user, self.email, self.first_name, self.last_name, self.gender, self.date_of_birth, 
        self.relationship_to_insured, self.air_id, self.mailing_street, self.mailing_city, self.mailing_state, 
        self.mailing_zip, self.residence_country, self.foreign_currency_default, self.other_coverage, 
        self.medicare_part_a, self.medicare_part_b]
        if all(required_fields):
            return True


class DependentProfile(Profile):
    
    created = models.DateTimeField(editable=False)
    # better related name would be dependent_profiles
    insured = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dependents')
    #base_profile = models.OneToOneField(Profile, on_delete=None)

    def save(self, *args, **kwargs):
        """ On save, populate created field with timestamp """
        if not self.id:
            self.created = timezone.now()
        return super(DependentProfile, self).save(*args, **kwargs)


    @property
    def profile_complete(self):
        required_fields = self._meta.fields
        """
        [self.insured, self.first_name, self.last_name, self.gender, self.date_of_birth, self.relationship_to_insured,
        self.residence_country, self.foreign_currency_default, self.other_coverage, self.medicare_part_a, self.medicare_part_b, 
        self.full_time_student, self.has_dependent]
        """
        if all(required_fields):
            return True
        
    class Meta:
        verbose_name = 'Dependent Profile'
        verbose_name_plural = 'Dependent Profiles'


class Report(models.Model):
    created = models.DateTimeField(editable=False)
    insured_profile = models.ForeignKey(InsuredProfile, on_delete=models.PROTECT, null=False, related_name='reports')
    dependent_profile = models.ForeignKey(DependentProfile, on_delete=models.PROTECT, null=True)
    diagnosis = models.CharField('Diagnosis', max_length=64, null=False)
    employment_related = models.CharField('Due to employment-related accident?', max_length=3, choices=AFFIRM_CHOICES, null=False, default='N')
    auto_accident_related = models.CharField('Due to auto accident?', max_length=3, choices=AFFIRM_CHOICES, null=False, default='N')
    other_accident_related = models.CharField('Due to other accident?', max_length=3, choices=AFFIRM_CHOICES, null=False, default='N')
    accident_date = models.DateTimeField('Accident/Onset Date', default=None, null=True, blank=True)
    accident_details = models.CharField('Accident Details', max_length=255, default=None, null=True, blank=True)
    full_time_student = models.CharField('Was patient full-time student at time of service?', max_length=1, choices=AFFIRM_CHOICES, default='N')
    school_name = models.CharField('School Name', max_length=128, default=None, null=True, blank=True)
    submitted = models.BooleanField(default=False, null=False)
    patient_slug = models.SlugField(unique=False)  

    
    def save(self, *args, **kwargs):
        """On save, create timestamp, populate patient_profile?"""
        if not self.id:
            self.created = timezone.now()
            print('report created at {}'.format(self.created))
        return super(Report, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __repr__(self):
       return (f'{self.__class__.__name__}('
                    f'{self.patient_slug!r} {self.created!r})')


class Claim(models.Model):
    CLAIM_TYPE_CHOICES = (
                                            ('M', 'Medical'),
                                            ('D', 'Dental'),
                                            ('V', 'Vision'),
                                            ('H', 'Hearing'),
                                            ('Rx', 'Prescription')
                                            )
    created = models.DateTimeField(editable=False)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='claims', blank=True)
    # tried to avoid repeating this in both Report and Claim - does it matter?
    insured_profile = models.ForeignKey(InsuredProfile, on_delete=models.PROTECT, null=False)
    dependent_profile = models.ForeignKey(DependentProfile, on_delete=models.PROTECT, null=True)

    claim_type = models.CharField('Claim Type', max_length=2, choices=CLAIM_TYPE_CHOICES)
    service_date = models.DateField('Date of Service', null=False)
    service_description = models.CharField('Description of Service', max_length=64, null=False)
    service_place = models.CharField('Place of Service', max_length=64, null=False)
    foreign_charges = models.DecimalField('Foreign Charges', max_digits=18, decimal_places=2)
    foreign_currency = models.CharField('Foreign Currency', max_length=64, choices=CURRENCY_CHOICES, null=False)
    exchange_rate = models.DecimalField('Exchange Rate', max_digits=30, decimal_places=10)
    usd_charges = models.DecimalField('USD Charges', max_digits=18, decimal_places=2)
    receipt_file = models.FileField('Receipt as Pdf', upload_to='store/', null=True, blank=True)
    receipt_image = models.ImageField('Receipt as Image', upload_to='store/', null=True, blank=True)
    #receipt_uploaded = models.BooleanField(default=False)
    #receipt_uploaded_at = models.DateTimeField(editable=False)


    # may not want to do this, and/or it may need to be done before saving - just want to show it in the form
    def save(self, *args, **kwargs):
        """
        On save, populate full_time_student field
        """
        #reports = Report.objects.filter(submitted=False)
        # fix this later 
        #self.report = reports[0]
        # for report in reports:
        if not self.id:
            self.created = timezone.now()
        #if self.dependent_profile:
            #self.full_time_student = self.dependent_profile.full_time_student
        conversion = CurrencyRates()
        self.exchange_rate = conversion.get_rate('USD', self.foreign_currency, self.service_date)
        self.usd_charges = float(self.foreign_charges) / self.exchange_rate

        return super(Claim, self).save(*args, **kwargs)



