from pass_app.main.models import UserVisited, UserProfile
from django.contrib import admin

admin.site.register(UserProfile)


class UserVisitedAdmin(admin.ModelAdmin):
    class Meta:
        model = UserVisited

    search_fields = ["user__user__username"]
    list_display = ("user", "section", "visited_time")

admin.site.register(UserVisited, UserVisitedAdmin)
