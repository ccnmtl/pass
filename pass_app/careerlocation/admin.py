from pass_app.careerlocation.models import Actor, ActorQuestion, \
    ActorResponse, CareerLocationState, MapLayer, Strategy
from django.contrib import admin

admin.site.register(MapLayer)
admin.site.register(Actor)
admin.site.register(Strategy)


class ActorQuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = ActorQuestion
        ordering = ['question']

    search_fields = ["question", "answer"]
    list_display = ("question", "answer")

admin.site.register(ActorQuestion, ActorQuestionAdmin)


class ActorResponseAdmin(admin.ModelAdmin):
    class Meta:
        model = ActorResponse

    search_fields = ["user__username"]
    list_display = ("user", "actor", "question")

admin.site.register(ActorResponse, ActorResponseAdmin)


class CareerLocationStateAdmin(admin.ModelAdmin):
    class Meta:
        model = CareerLocationState

    search_fields = ["user__username"]

admin.site.register(CareerLocationState, CareerLocationStateAdmin)
