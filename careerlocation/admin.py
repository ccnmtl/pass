from careerlocation.models import *
from django.contrib import admin

admin.site.register(MapLayer)
admin.site.register(ActorQuestion)
admin.site.register(Actor)

class ActorResponseAdmin(admin.ModelAdmin):
    class Meta:
        model = ActorResponse

    search_fields = ["user__username"]
    list_display = ("user","actor","question")

admin.site.register(ActorResponse, ActorResponseAdmin)

class CareerLocationStateAdmin(admin.ModelAdmin):
    class Meta:
        model = CareerLocationState

    search_fields = ["user__username"]

admin.site.register(CareerLocationState, CareerLocationStateAdmin)