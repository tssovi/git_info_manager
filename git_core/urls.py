from django.urls import path
from git_core.views import home, git_profile, link_github, callback, repo_list, create_hook, webhook, activity


urlpatterns = [
    path('', home, name='home'),
    path('git-profile/', git_profile, name='git-profile'),
    path('link-github/', link_github, name="link-github"),
    path('callback/', callback, name='callback'),
    path('repo-list/', repo_list, name='repo-list'),
    path('create-hook/<str:repo_id>/', create_hook, name='create-hook'),
    path('webhook/<str:login>/', webhook, name='webhook'),
    path('activity/', activity, name='activity'),
]
