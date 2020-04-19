from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime


class GithubProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=40, null=True)
    email = models.CharField(_('Email'), max_length=40, null=True)
    public_repos = models.CharField(_('Public Repo Count'), max_length=5)
    login = models.CharField(_('Login'), max_length=30, null=True)
    avatar_url = models.URLField(_('Avatar Url'), max_length=500, null=True)
    repos_url = models.URLField(_('Repos Url'), max_length=500, null=True)
    html_url = models.URLField(_('HTML Url'), max_length=500, null=True)
    access_token = models.CharField(_('Access Token'), max_length=500, null=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name_plural = 'Github Profile'

    def __str__(self):
        return "Github Profile details data inserted on {date}".format(
            date=datetime.strftime(self.created_at, "%B %d,%Y")
        )


class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_id = models.CharField(_('Repo Id'), max_length=150, null=True)
    name = models.CharField(_('Repo Name'), max_length=500, null=True)
    full_name = models.CharField(_('Repo Full Name'), max_length=500, null=True)
    html_url = models.URLField(_('Html Url'), max_length=500, null=True)
    description = models.TextField(_('Description'), null=True)
    url = models.URLField(_('Url'), max_length=500, null=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name_plural = 'Repository'

    def __str__(self):
        return "Repository details data inserted on {date}".format(
            date=datetime.strftime(self.created_at, "%B %d,%Y")
        )


class Hooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    hook_id = models.CharField(_('Hook Id'), max_length=150, null=True)
    test_url = models.URLField(_('Test Url'), max_length=500, null=True)
    ping_url = models.URLField(_('Ping Url'), max_length=500, null=True)
    name = models.CharField(_('Name'), max_length=500, null=True)
    events = models.TextField(('Events'), null=True)
    active = models.CharField(_('Active'), max_length=150, null=True)
    config = models.TextField(_('Config'), null=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Update at'), auto_now=True)

    class Meta:
        verbose_name_plural = 'Hooks'

    def __str__(self):
        return "Hooks details data inserted on {date}".format(
            date=datetime.strftime(self.created_at, "%B %d,%Y")
        )


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField(('Details'), null=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Activity'

    def __str__(self):
        return "Activity details data inserted on {date}".format(
            date=datetime.strftime(self.created_at, "%B %d,%Y")
        )

