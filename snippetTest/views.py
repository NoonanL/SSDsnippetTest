from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import bleach
from snippetTest.models import Snippet
from django.db.models import Q

# Create your views here.

def loginView(request):
	# users = User.objects.all()
	# return render(request, 'login.html')
	if request.method == 'GET':
		return render(request, 'login.html')
	elif request.method == 'POST':
		selection = request.POST['button']
	
	#If the button pressed is create new user
	if selection == 'Create User':
		username = bleach.clean(request.POST['username'])
		password = bleach.clean(request.POST['password'])
		if username == '' or password == '' or len(username) > 15 or len(username) < 3 or len(password) > 15 or len(password) < 6:
			messages.warning(request, 'Username or Password do not meet the minimum requirements.')
			return redirect('/login/')
			# return HttpResponseRedirect('/home/', {'error':error})
		else:
			if User.objects.filter(username=username).exists():
				messages.warning(request, 'Username or Password do not meet the minimum requirements.')
				return redirect('/login/')
			else:
				user = User.objects.create_user(username, "", password)
				# messages.warning(request, 'Account created, you may now Log In.')
				loggedUser = authenticate(request, username = username, password = password)
				if user is not None:
					login(request, loggedUser)
					return redirect('/home/')
				else:
					messages.warning(request, 'Not a valid User.')
					return redirect('/login/')
				# return redirect('/login/')

	#If the button pressed is Login		
	if selection == 'Login':
		username = bleach.clean(request.POST['username'])
		password = bleach.clean(request.POST['password'])
		if username == '' or password == '' :
			messages.warning(request, 'Invalid Username or Password.')
			return redirect('/login/')
		else:
			user = authenticate(request, username = username, password = password)
			if user is not None:
				login(request, user)
				return redirect('/home/')
			else:
				messages.warning(request, 'Not a valid User.')
				return redirect('/login/')
	else:
		return redirect('/login/')


def homeView(request):
	if request.user.is_authenticated:
		username = request.user.username
		allSnippets = Snippet.objects.filter(uploadUser=username)
		#print(allSnippets)
		print('Authenticated!')
		return render(request, 'home.html',{'username':username,'allSnippets':allSnippets})
	else:
		print('Not authenticated, redirecting to login')
		return redirect('/login/')

def submitLogout(request):
	logout(request)
	return redirect('/login/')

def deleteSnippet(request, snippetId):
	if ((request.method == 'POST') and (request.user.is_authenticated == True)):
		username = request.user.username
		deleteSnippet = Snippet.objects.get(id=snippetId)
		if(deleteSnippet.uploadUser == username):
			deleteSnippet.delete()
			return redirect('/home/')
		else:
			allSnippets = Snippet.objects.filter(uploadUser=username)
			return render(request, 'home.html', {'username':username,
										'message':'You do not have authorisation to delete that Snippet!',
										'allSnippets':allSnippets})
	else:
		return redirect('/home/')


def openSnippet(request, snippetId):
	if ((request.method == 'POST') and (request.user.is_authenticated == True)):
		username = request.user.username
		openSnippet = Snippet.objects.get(id=snippetId)
		return render(request, 'editSnippet.html', {'username':username,
								'snippet':openSnippet})
	else:
		return redirect('/home/')


def editSnippet(request, snippetId):
	if ((request.method == 'POST') and (request.user.is_authenticated == True)):
		username = request.user.username
		openSnippet = Snippet.objects.get(id=snippetId)
		uploadSnippet = request.POST['editedSnippet']
		
		if len(uploadSnippet) > 0 and len(uploadSnippet) < 1024:
			openSnippet.editedSnippet = uploadSnippet
			openSnippet.editedBy = username
			openSnippet.save()
			cleanSnippet = bleach.clean(uploadSnippet)
			return render(request, 'editSnippet.html', {'username':username,
								'snippet':openSnippet,
								'cleanSnippet':cleanSnippet,
								'message':'We have quarantined your edit as it may contain malicious code. Your sanitised code snippet is:'
								})
		
	else:
		return redirect('/home/')


def uploadView(request):
	if request.user.is_authenticated:
		username = request.user.username
		if request.method == 'GET':
			return render(request, 'upload.html', {'username':username})
		if request.method == 'POST':
			uploadSnippet = request.POST['snippetInput']
		snippetTitle = request.POST['snippetTitle']
		snippetLanguage = request.POST['snippetLanguage']
		if len(uploadSnippet) > 0 and len(uploadSnippet) < 1024 and len(snippetTitle) > 0 and len(snippetTitle) < 30 and len(snippetLanguage) > 0 and len(snippetLanguage) < 20 :
			newSnippet = Snippet(uploadUser=username,originalSnippet=uploadSnippet,title=snippetTitle,language=snippetLanguage)
			newSnippet.save()
			allSnippets = Snippet.objects.filter(uploadUser=username)
			cleanSnippet = bleach.clean(request.POST['snippetInput'])
			return render(request, 'upload.html', {'username':username,
											'cleanSnippet':cleanSnippet,
											'message':'We have quarantined your snippet as it may contain malicious code. Your sanitised code snippet is:',
											'allSnippets':allSnippets})
		else:
			messages.warning(request, 'Please fill out all fields.')
			return redirect('/upload/')
	else:
		return redirect('/login/')



def viewSnippets(request):
	if (request.user.is_authenticated == True):
		if request.method == 'POST':
			searchStr = request.POST['searchStr']
		else:
			searchStr = ""
		username = request.user.username
		#cleanSearch = bleach.clean(searchStr)
		if len(searchStr) < 20:
			allSnippets = Snippet.objects.filter(Q(originalSnippet__contains=searchStr) | Q(title__contains=searchStr) | Q(language__contains=searchStr))
			return render(request, 'viewSnippets.html', {'username':username,
														'allSnippets':allSnippets})
		else:
			messages.warning(request, 'Search query too long!')
			return redirect('/searchSnippets/')
	else:
		return redirect('/login/')

	