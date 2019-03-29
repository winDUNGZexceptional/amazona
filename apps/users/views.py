from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.users.forms import RegisterForm, LoginForm
from apps.users.models import User

# Create your views here.



def index(request):

	registration_form = RegisterForm()
	login_form = LoginForm()

	context = {
	'registration_form' : registration_form,
	'login_form' : login_form,
	}
	return render(request, 'users/pages/index.html', context)


def register(request):
	
	if request.method == 'POST':

		registration = RegisterForm(request.POST)

		if registration.is_valid():

			print(registration.cleaned_data.get('confirm_password'))

			new_user = User.objects.create(
				name = registration.cleaned_data.get('name'),
				alias = registration.cleaned_data.get('alias'),
				email = registration.cleaned_data.get('email'),
				password = registration.cleaned_data.get('confirm_password')
				)

			messages.success(request, 'Registration Success')
			return HttpResponseRedirect( reverse('users:index') )

		else:
			print(registration.errors)
			return HttpResponseRedirect( reverse('users:index') )


	else:
		print('not allowed!')
		messages.error(request, 'You are not allowed here.')
		return HttpResponseRedirect( reverse('users:index'))


def login(request):	
	
	if request.method == 'POST':

		login_form = LoginForm(request.POST)

		if login_form.is_valid():

			user_logging = User.objects.filter(
				email = login_form.cleaned_data.get('email')
				).first()

			if user_logging is not None:

				is_authenticated = check_password(
					login_form.cleaned_data.get('password'),
					user_logging.password
					)

				if is_authenticated:
					
					user_details = {
					'id' : user_logging.id,
					'name' : user_logging.name,
					'alias' : user_logging.alias,
					'email' : user_logging.email,
					}

					request.session['is_authenticated'] = True
					request.session['user'] = user_details

					messages.success(request, 'Welcome ' + user_logging.name + '!')
					return HttpResponseRedirect( reverse('books:list') )

				else:
					messages.error(request, 'Invalid username and password.')
					return HttpResponseRedirect( reverse('users:index') )
						
					

			else:
				messages.error(request, 'Invalid username and password.')
				return HttpResponseRedirect( reverse('users:index') )


		else:
			print('invalid!')
			messages.error(request, 'Invalid email format or password.')
			return HttpResponseRedirect( reverse('users:index') )
	else:
		messages.error(request, 'You are not allowed to this page.')
		return HttpResponseRedirect( reverse('users:index') )


def logout(request):
	
	is_authenticated = request.session.get('is_authenticated', False)

	if is_authenticated:

		request.session.pop('user')
		request.session.pop('is_authenticated')

		messages.success(request, 'Logged out.')
		return HttpResponseRedirect( reverse('users:index') )

	else:

		messages.error(request, 'You are not yet logged in.')
		return HttpResponseRedirect( reverse('users:index') )


def show_user(request, user_id):

	user = User.objects.filter(id = user_id).first()

	if user is not None:
		
		context = {
		'user' : user,
		}
		return render(request, 'users/pages/show.html', context)

	else:
		messages.error(request, 'User does not exists.')
		return HttpResponseRedirect( reverse('books:list') )