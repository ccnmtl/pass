from django.db import models
from django.contrib.auth.models import User
from pagetree.models import Section


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    last_location = models.CharField(max_length=255, default="/")

    def __unicode__(self):
        return self.user.username

    def display_name(self):
        return self.user.username

    def save_visit(self, section):
        self.last_location = section.get_absolute_url()
        self.save()
        uv, created = UserVisited.objects.get_or_create(
            profile=self, section=section)

    def save_visits(self, sections):
        for s in sections:
            self.save_visit(s)

    def has_visited(self, section):
        return UserVisited.objects.filter(
            profile=self, section=section).count() > 0


class UserVisited(models.Model):
    profile = models.ForeignKey(UserProfile)
    section = models.ForeignKey(Section)
    visited_time = models.DateTimeField(auto_now=True)
