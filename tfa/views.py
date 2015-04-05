from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

import pyotp
import urlparse

from .models import User

class RegisterForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=30)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput())
	tfaToken = forms.CharField(label='TFA Token', max_length=6)
# Create your views here.

def index(request):
	user_list = User.objects.all()
	context = {'user_list': user_list}
	return render(request, 'tfa/index.html', context)

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			seed = pyotp.TOTP(pyotp.random_base32())
			# The parameter below is used as the label for the auth app interface.
			uri = seed.provisioning_uri(username)
			secret = urlparse.parse_qs(urlparse.urlparse(uri).query)['secret'][0]

			# This can fail if username is not unique. TODO: wrap in try
			newUser = User(username=username, password=password, tfaEnabled=True, tfaSecret=secret)
			newUser.save()

			request.session['username'] = username
			request.session['password'] = password
			request.session['tfaUri'] = uri

			return redirect(reverse('tfaSetup'))
		else:
			return render(request, 'tfa/register.html', {'form': RegisterForm()})
	else:
		return render(request, 'tfa/register.html', {'form': RegisterForm()})

def tfaSetup(request):
	return render(request, 'tfa/tfaSetup.html', {
		'username': request.session.get('username'),
		'tfaUri': request.session.get('tfaUri')
	})

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			user = User.objects.filter(
				username__exact=form.cleaned_data['username']
			).get()

			print(user)

			if not user:
				return HttpResponse("No such user!")

			if user.password != form.cleaned_data['password']:
				return HttpResponse("Bad password!")

			expectedToken = "%06d" % pyotp.TOTP(user.tfaSecret).now()
			if form.cleaned_data['tfaToken'] != str(expectedToken):
				return HttpResponse("Bad TFA token! Expected " + str(expectedToken) + ", got " + form.cleaned_data['tfaToken'])

			return redirect(reverse('landing', kwargs={'user_id': user.id}))
		else:
			return render(request, 'tfa/login.html', {'form': LoginForm()})
	else:
		return render(request, 'tfa/login.html', {'form': LoginForm()})

def landing(request, **kwargs):
	user = User.objects.filter(
		id__exact=kwargs.get('user_id')
	).get()
	return render(request, 'tfa/landing.html', {'username': user.username})


