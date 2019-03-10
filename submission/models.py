from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
#from django.contrib.auth import get_user_model

from .geography_lists import us_states, countries, currencies

from datetime import datetime
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
    auto_increment_id = models.AutoField(primary_key=True)
    # will be foreign key taken from User model
    # not sure if null and blank should really be True here?
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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
    date_of_birth = models.DateField('Date of Birth')
    air_id = models.CharField('AIR ID', max_length=20)
    mailing_street = models.CharField('Mailing - Street', max_length=64)
    mailing_optional = models.CharField('Mailing - Optional', max_length=64, null=True, blank=True)
    mailing_city = models.CharField('Mailing - City', max_length=64)
    mailing_state = models.CharField('Mailing - State', max_length=32, choices=US_STATE_CHOICES)
    mailing_zip = models.CharField('Mailing - Zip', max_length=10)
    mailing_country = models.CharField('Mailing - Country', max_length=64, choices=COUNTRY_CHOICES)
    residence_country = models.CharField('Residence - Country', max_length=64, choices=COUNTRY_CHOICES)
    foreign_currency_default = models.CharField('Foreign Currency Default', max_length=64, choices=CURRENCY_CHOICES)
    other_coverage = models.CharField('Other health insurance coverage?', max_length=3, choices=AFFIRM_CHOICES)
    other_insurance_co = models.CharField('Other health insurance provider', max_length=64, null=True, blank=True)
    other_plan_name = models.CharField('Other health plan name', max_length=64, null=True, blank=True)
    other_plan_id = models.CharField('Other health plan id', max_length=64, null=True, blank=True)
    medicare_part_a = models.CharField('Medicare Part A coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True, blank=True)
    medicare_part_b = models.CharField('Medicare Part B coverage?', max_length=3, choices=AFFIRM_CHOICES, null=True, blank=True)
    medicare_id = models.CharField('Medicare ID', max_length=64, null=True, blank=True)
    full_time_student = models.CharField('Is insured full-time student?', max_length=3, choices=AFFIRM_CHOICES)
    has_dependent = models.CharField('Does insured have dependents?', max_length=3, choices=AFFIRM_CHOICES)
    
    # leftover from Flask?
    #not a db field but high-level view of relationship 
    #between insureds and claims - a 'virtual field'
    #claims = db.relationship('Claim', backref='author', lazy='dynamic')
    #dependents = db.relationship('Dependent', backref='employee', lazy='dynamic')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('create_user_profile', kwargs={'pk' : self.pk})
    

# form works just fine without this as long as fields are defined in the view
class InsuredProfileForm(forms.ModelForm):
    class Meta:
        model = InsuredProfile
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'gender',
                    'date_of_birth', 'air_id', 'mailing_street', 'mailing_optional', 'mailing_city',
                    'mailing_state', 'mailing_zip', 'mailing_country', 'residence_country',
                    'foreign_currency_default', 'other_coverage', 'other_insurance_co',
                    'other_plan_name', 'other_plan_id', 'medicare_part_a', 'medicare_part_b',
                    'medicare_id', 'full_time_student', 'has_dependent']
        widgets = {
                'description': forms.Textarea(),
        }



    # modify for Django or delete - probably taken care of in User for Django
    """
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], 
                algorithms=['HS256'])['reset_password']
        except:
            return
        return Insured.query.get(id)

"""