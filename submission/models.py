from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model

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


# copied from Flask app - modify for Django
class InsuredProfile(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    # will be foreign key taken from User model
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    # email may also be taken from User if requested at sign up
    email = models.EmailField(max_length=120)
    #password_hash = models.CharField(max_length=128)
    last_seen = models.DateTimeField(default=datetime.utcnow)
    # may also be taken from User?
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64)
    # may also be taken from User?
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, help_text="Enter 'M' or 'F'")
    date_of_birth = models.DateField()
    air_id = models.CharField(max_length=20)
    mailing_street = models.CharField(max_length=64)
    mailing_optional = models.CharField(max_length=64)
    mailing_city = models.CharField(max_length=64)
    mailing_state = models.CharField(max_length=15)
    mailing_zip = models.CharField(max_length=10)
    mailing_country = models.CharField(max_length=64)
    residence_country = models.CharField(max_length=64)
    foreign_currency_default = models.CharField(max_length=64)
    other_coverage = models.CharField(max_length=1, help_text="Enter 'Y' or 'N'")
    other_insurance_co = models.CharField(max_length=64)
    other_plan_name = models.CharField(max_length=64)
    other_plan_id = models.CharField(max_length=64)
    medicare_part_a = models.CharField(max_length=1, help_text="Enter 'Y' or 'N'")
    medicare_part_b = models.CharField(max_length=1, help_text="Enter 'Y' or 'N'")
    medicare_id = models.CharField(max_length=64)
    full_time_student = models.CharField(max_length=1, help_text="Enter 'Y' or 'N'")
    has_dependent = models.CharField(max_length=1, help_text="Enter 'Y' or 'N'")
    
    # leftover from Flask?
    #not a db field but high-level view of relationship 
    #between insureds and claims - a 'virtual field'
    #claims = db.relationship('Claim', backref='author', lazy='dynamic')
    #dependents = db.relationship('Dependent', backref='employee', lazy='dynamic')

    def __str__(self):
        return self.username
    

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