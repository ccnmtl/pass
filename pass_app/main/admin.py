from pass_app.main.models import UserVisited, UserProfile
from django.contrib import admin
from pagetree.models import Hierarchy

admin.site.register(UserProfile)


def section_hierarchy_name(obj):
    return obj.section.hierarchy

section_hierarchy_name.short_description = 'Hierarchy'


class UserVisitedAdmin(admin.ModelAdmin):
    class Meta:
        model = UserVisited

    search_fields = ["user__user__username"]
    list_display = ("user", "section", section_hierarchy_name, "visited_time")

admin.site.register(UserVisited, UserVisitedAdmin)

admin.site.register(Hierarchy)
