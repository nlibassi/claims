from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.urls import reverse
from django import forms
#from django.contrib.auth import get_user_model

from .geography_lists import us_states, countries, currencies

from datetime import datetime

from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Products(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(default=0.00, max_digits=18, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tutorial_products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Sales(models.Model):
    product = models.ForeignKey(Products, on_delete=None)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=18, decimal_places=2)
    customer = models.ForeignKey(User, on_delete=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super(Sales, self).save(*args, **kwargs)

    class Meta:
        db_table = "tutorial_product_sales"
        verbose_name = "Sale"
        verbose_name_plural = "Sales"



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
('male', 'M'),
('female', 'F')
)
AFFIRM_CHOICES = (
    ('yes', 'YES'),
    ('no', 'NO')
    )
US_STATE_CHOICES = tuple(us_states)
COUNTRY_CHOICES = tuple(countries)
CURRENCY_CHOICES = tuple(currencies)

# copied from Flask app - modify for Django, blank=True
class InsuredProfile(models.Model):
    #auto_increment_id = models.AutoField(primary_key=True)
    # probably don't need to add unique here
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    # email may also be taken from User if requested at sign up
    email = models.EmailField(max_length=120)
    #password_hash = models.CharField(max_length=128)
    last_seen = models.DateTimeField(default=datetime.utcnow)
    # may also be taken from User?
    first_name = models.CharField('First Name', max_length=64)
    middle_name = models.CharField('Middle Name', max_length=64)
    # may also be taken from User?
    last_name = models.CharField('Last Name', max_length=64)
    gender = models.CharField('Gender', max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField('Date of Birth', null=True)
    air_id = models.CharField('AIR ID', max_length=20, null=True, unique=True)
    mailing_street = models.CharField('Mailing - Street', max_length=64, null=True)
    mailing_optional = models.CharField('Mailing - Optional', max_length=64, null=True, blank=True)
    mailing_city = models.CharField('Mailing - City', max_length=64, null=True)
    mailing_state = models.CharField('Mailing - State', max_length=32, choices=US_STATE_CHOICES, null=True)
    mailing_zip = models.CharField('Mailing - Zip', max_length=10, null=True)
    #mailing_country = models.CharField('Mailing - Country', max_length=64, choices=COUNTRY_CHOICES, null=True)
    residence_country = models.CharField('Residence - Country', max_length=64, choices=COUNTRY_CHOICES, null=True)
    foreign_currency_default = models.CharField('Foreign Currency Default', max_length=64, choices=CURRENCY_CHOICES, null=True)
    other_coverage = models.CharField('Other health insurance coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True)
    other_insurance_co = models.CharField('Other health insurance provider', max_length=64, null=True, blank=True)
    other_plan_name = models.CharField('Other health plan name', max_length=64, null=True, blank=True)
    other_plan_id = models.CharField('Other health plan id', max_length=64, null=True, blank=True)
    medicare_part_a = models.CharField('Medicare Part A coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True)
    medicare_part_b = models.CharField('Medicare Part B coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True)
    medicare_id = models.CharField('Medicare ID', max_length=64, null=True, blank=True)
    full_time_student = models.CharField('Is insured full-time student?', max_length=3, choices=AFFIRM_CHOICES)
    has_dependent = models.CharField('Does insured have dependents?', max_length=3, choices=AFFIRM_CHOICES)
    
    # leftover from Flask?
    #not a db field but high-level view of relationship 
    #between insureds and claims - a 'virtual field'
    #claims = db.relationship('Claim', backref='author', lazy='dynamic')
    #dependents = db.relationship('Dependent', backref='employee', lazy='dynamic')

    def __str__(self):
        return str(self.user)

    # not sure if this function should stay - may not matter as using try/except when completing/updating profile
    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            insured_profile = InsuredProfile(user=user)
            insured_profile.save()
            
    post_save.connect(create_profile, sender=User)

    @property
    def profile_complete(self):
        required_fields = [self.user, self.email, self.first_name, self.last_name, self.gender, self.date_of_birth, self.air_id,
        self.mailing_street, self.mailing_city, self.mailing_state, self.mailing_zip, self.residence_country,
        self.foreign_currency_default, self.other_coverage, self.medicare_part_a, self.medicare_part_b, self.full_time_student, 
        self.has_dependent]
        if all(required_fields):
            return True
        
    class Meta:
        verbose_name = 'Insured Profile'
        verbose_name_plural = 'Insured Profiles'


class DependentProfile(models.Model):
    RELATIONSHIP_CHOICES = (
                                            ('spouse', 'Spouse'),
                                            ('child', 'Child')
                                            )
    insured = models.ForeignKey(User, on_delete=None, related_name='dependents')
    first_name = models.CharField('First Name', max_length=64)
    middle_name = models.CharField('Middle Name', max_length=64)
    last_name = models.CharField('Last Name', max_length=64)
    gender = models.CharField('Gender', max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField('Date of Birth', null=True)
    relationship_to_insured = models.CharField('Relationship to insured', max_length=6, choices=RELATIONSHIP_CHOICES)
    residence_country = models.CharField('Residence - Country', max_length=64, choices=COUNTRY_CHOICES, null=True)
    foreign_currency_default = models.CharField('Foreign Currency Default', max_length=64, choices=CURRENCY_CHOICES, null=True)
    other_coverage = models.CharField('Other health insurance coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True)
    other_insurance_co = models.CharField('Other health insurance provider', max_length=64, null=True, blank=True)
    other_plan_name = models.CharField('Other health plan name', max_length=64, null=True, blank=True)
    other_plan_id = models.CharField('Other health plan id', max_length=64, null=True, blank=True)
    medicare_part_a = models.CharField('Medicare Part A coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True)
    medicare_part_b = models.CharField('Medicare Part B coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True)
    medicare_id = models.CharField('Medicare ID', max_length=64, null=True, blank=True)
    full_time_student = models.CharField('Is insured full-time student?', max_length=3, choices=AFFIRM_CHOICES)

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





