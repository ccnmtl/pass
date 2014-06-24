from django import forms
from django.contrib import admin
from pass_app.supportservices.models import SupportService, \
    SupportServiceCategory


class SupportServiceForm(forms.ModelForm):
    class Meta:
        model = SupportService
        widgets = {
            'title': admin.widgets.AdminTextInputWidget
        }


class SupportServiceAdmin(admin.ModelAdmin):
    form = SupportServiceForm

admin.site.register(SupportService, SupportServiceAdmin)
admin.site.register(SupportServiceCategory)
