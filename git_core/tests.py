from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from git_core.views import home, git_profile, link_github, callback, repo_list, create_hook, webhook, activity

class GitCoreTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_git_profile_view_status_code(self):
        url = reverse('git-profile')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_git_profile_url_resolves_home_view(self):
        view = resolve('/git-profile/')
        self.assertEquals(view.func, git_profile)

    def test_link_github_view_status_code(self):
        url = reverse('link-github')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_link_github_url_resolves_home_view(self):
        view = resolve('/link-github/')
        self.assertEquals(view.func, link_github)

    def test_callback_view_status_code(self):
        url = reverse('callback')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_callback_url_resolves_home_view(self):
        view = resolve('/callback/')
        self.assertEquals(view.func, callback)

    def test_repo_list_view_status_code(self):
        url = reverse('repo-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_repo_list_url_resolves_home_view(self):
        view = resolve('/repo-list/')
        self.assertEquals(view.func, repo_list)

    def test_activity_view_status_code(self):
        url = reverse('activity')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_activity_url_resolves_home_view(self):
        view = resolve('/activity/')
        self.assertEquals(view.func, activity)

