from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import bleach

# Create your views here.

def loginView(request):
	users = User.objects.all()
	return render(request, 'login.html')

def submitLogin(request):

#Reject GET requests for this page. 
	if request.method == 'GET':
		return redirect('/login/')
	elif request.method == 'POST':
		selection = request.POST['button']

	error = ''
	
	#If the button pressed is create new user
	if selection == 'Create User':
		username = bleach.clean(request.POST['username'])
		password = bleach.clean(request.POST['password'])
		if username == '' or password == '' :
			error = 'Invalid Username or Password, cannot create account!'
			return render(request, 'login.html', {'error':error})
			# return HttpResponseRedirect('/home/', {'error':error})
		else:
			user = User.objects.create_user(username, "", password)
			messages.warning(request, 'Account created, you may now Log In.')
			return redirect('/login/')

	#If the button pressed is Login		
	if selection == 'Login':
		username = bleach.clean(request.POST['username'])
		password = bleach.clean(request.POST['password'])
		if username == '' or password == '' :
			error = 'Invalid Username or Password!'
			return render(request, 'login.html', {'error':error})
		else:
			user = authenticate(request, username = username, password = password)
			if user is not None:
				login(request, user)
				return redirect('/home/')
			else:
				error = "Not a valid User"
				messages.warning(request, 'Not a valid User.')
				return redirect('/login/')
	else:
		return redirect('/login/')

def homeView(request):
	username = request.user.username
	if request.user.is_authenticated:
		print('Authenticated!')
		return render(request, 'home.html',{'username':username})
	else:
		print('Not authenticated, redirecting to login')
		return redirect('/login/')

def submitLogout(request):
	logout(request)
	return redirect('/login/')

def testSnippet(request):
	if request.method == 'GET':
		return redirect('/home/')
	elif request.method == 'POST':
		if request.user.is_authenticated == 'false':
			return redirect('/login/')
		else:
			cleanSnippet = bleach.clean(request.POST['snippetInput'])
			return render(request, 'home.html', {'cleanSnippet':cleanSnippet,'message':'Your sanitised code snippet is:'})

	