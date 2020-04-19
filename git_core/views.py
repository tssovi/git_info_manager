import json
import requests
import urllib
from git_core.models import *
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from git_manager.settings import CLIENT_ID, CLIENT_SECRET, NGROK_URL


def home(request):
	return render(request, 'pages/home.html')


@login_required
def git_profile(request):
	if len(request.user.githubprofile_set.all())==1:
		return HttpResponseRedirect('/repo-list/')
	else:
		return HttpResponseRedirect('/link-github/')


@login_required
def link_github(request):
	url = 'https://github.com/login/oauth/authorize/?client_id={}&scope=user:email,public_repo' \
		  '&state=sheesh'.format(CLIENT_ID)
	return HttpResponseRedirect(url)


@login_required
def callback(request):
	code = request.GET.get('code')
	# state = request.GET.get('state')
	payload = {'client_id':CLIENT_ID, 'client_secret':CLIENT_SECRET, 'code':code}
	response = requests.post('https://github.com/login/oauth/access_token', params=payload)
	response = urllib.parse.parse_qs(response.text)
	access_token = response['access_token'][0]
	request.session['access_token'] = access_token
	url = 'https://api.github.com/user?access_token=' + str(access_token)
	response = requests.get(url)
	response = response.json()
	git_profile = GithubProfile(
		user=request.user,
		name=response["name"],
		email=response["email"],
		public_repos=response["public_repos"],
		login=response["login"],
		avatar_url = response["avatar_url"],
		repos_url= response["repos_url"],
		html_url=response["html_url"],
		access_token=access_token
	)
	git_profile.save()

	url = response["repos_url"]
	# public_repo_count = response["public_repos"]
	response = requests.get(url)
	repos = response.json()
	for repo in repos:
		git_repo = Repository(
			user=request.user,
			repo_id=repo["id"],
			name=repo["name"],
			full_name=repo["full_name"],
		 	html_url=repo["html_url"],
			description=repo["description"],
			url=repo["url"]
		)
		git_repo.save()
	return HttpResponseRedirect('/repo-list/')

@login_required
def repo_list(request):
	prof = request.user.githubprofile_set.all()[0]
	public_repo_count = prof.public_repos
	repos = request.user.repository_set.all()
	return render(request, 'pages/repo_list.html', context={'repos':repos, 'count':public_repo_count})

@login_required
def create_hook(request, repo_id):
	repo = request.user.repository_set.get(repo_id=repo_id)
	git_prof = request.user.githubprofile_set.all()[0]
	url = 'https://api.github.com/repos/{}/{}/hooks?access_token={}'\
		.format(git_prof.login, repo.name, git_prof.access_token)
	payload = """{"name": "web", "active": true, "events": [ "push", "pull_request" ],
			  "config": { "url": "%s/webhook/%s/", "content_type": "json" }}""" \
			  % (NGROK_URL, git_prof.login)
	headers = {'Content-Type': 'application/json'}
	response = requests.post(url, data=payload, headers=headers)
	response = response.json()
	try:
		hook = Hooks(
			user=request.user,
			repo=repo,
			hook_id=response["id"],
			test_url=response["test_url"],
			ping_url=response["ping_url"],
			name=response["name"],
			events=response["events"],
			active=response["active"],
			config=response["config"],
			updated_at=response["updated_at"],
			created_at=response["created_at"]
		)
		hook.save()
		return HttpResponseRedirect('/repo-list/')
	except Exception:
		message = "Error!!! Either This Repository Is Already Hooked Or Invalid Request. Please Try Again."
		return render(request, 'pages/error.html', context={'message': message})


@csrf_exempt
def webhook(request, login):
	response = request.body
	text_response = json.loads(response)
	git_user = GithubProfile.objects.get(login=login)
	activity = Activity(user=git_user.user, details=text_response)
	activity.save()
	message = "Activity Log Inserted Successfully."
	return render(request, 'pages/success.html', context={'message': message})

@login_required
def activity(request):
	activities = request.user.activity_set.all()
	return render(request, 'pages/activity.html', context={'activities':activities})

