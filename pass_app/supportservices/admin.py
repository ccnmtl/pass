from django import forms
from django.contrib import admin
from pass_app.supportservices.models import SupportService, \
    SupportServiceCategory, SupportServiceState


class SupportServiceForm(forms.ModelForm):
    class Meta:
        model = SupportService
        widgets = {
            'title': admin.widgets.AdminTextInputWidget
        }
        exclude = []


class SupportServiceAdmin(admin.ModelAdmin):
    form = SupportServiceForm

admin.site.register(SupportService, SupportServiceAdmin)
admin.site.register(SupportServiceCategory)
admin.site.register(SupportServiceState)
