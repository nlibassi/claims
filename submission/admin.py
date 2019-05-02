from django.contrib import admin
from .models import *

# should this go in models?
class InsuredProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)

class DependentProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'insured', 'relationship_to_insured',)

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
admin.site.register(InsuredProfile, InsuredProfileAdmin)
admin.site.register(DependentProfile, DependentProfileAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Claim, ClaimAdmin)