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

			newUser = User(username=username, password=password, tfaEnabled=True, tfaSecret=secret)
			newUser.save()

			request.session['username'] = username
			request.session['password'] = password
			request.session['tfaUri'] = uri

			return redirect(reverse('tfaSetup'))
		else:
			return render(request, 'tfa/register.html', {'form': RegisterForm()})
	else:
		form = RegisterForm()
		return render(request, 'tfa/register.html', {'form': form})

def tfaSetup(request):
	return render(request, 'tfa/tfaSetup.html', {
		'username': request.session.get('username'),
		'tfaUri': request.session.get('tfaUri')
	})

def login(request):
	return HttpResponse("You can log in here.")

def landing(request, request_id):
	return HttpResponse("You have successfully logged in!")