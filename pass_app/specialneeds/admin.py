from django.contrib import admin
from pass_app.specialneeds.models import SpecialNeedsCall, \
    SpecialNeedsCallState


class SpecialNeedsCallStateAdmin(admin.ModelAdmin):
    class Meta:
        model = SpecialNeedsCallState

    search_fields = ["user__username"]


admin.site.register(SpecialNeedsCall)
admin.site.register(SpecialNeedsCallState, SpecialNeedsCallStateAdmin)
