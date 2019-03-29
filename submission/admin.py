from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Sales)
admin.site.register(Products)
admin.site.register(InsuredProfile)
admin.site.register(DependentProfile)
admin.site.register(Report)
admin.site.register(Claim)