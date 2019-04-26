from django.contrib import admin
from .models import *

# should this go in models?
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ('patient_slug', 'submitted', 'id',)

class ClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_type', 'service_date', 'service_description',)

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
# Register your models here.

admin.site.register(Sales)
admin.site.register(Products)
admin.site.register(InsuredProfile)
admin.site.register(DependentProfile)
admin.site.register(Report, ReportAdmin)
admin.site.register(Claim, ClaimAdmin)