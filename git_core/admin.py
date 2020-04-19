from django.contrib import admin
from git_core.models import GithubProfile, Repository, Hooks, Activity


admin.site.register(GithubProfile)
admin.site.register(Repository)
admin.site.register(Hooks)
admin.site.register(Activity)