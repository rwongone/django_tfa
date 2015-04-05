from django.conf.urls import url

from . import views

urlpatterns = [
	# /tfa/
	url(r'^$', views.index, name='index'),
	# /tfa/register/
	url(r'^register/$', views.register, name='register'),
	# /tfa/tfaSetup/
	url(r'^tfaSetup/$', views.tfaSetup, name='tfaSetup'),
	# /tfa/login/
	url(r'^login/$', views.login, name='login'),
	# /tfa/1/
	url(r'^(?P<user_id>[0-9]+)/$', views.landing, name='landing'),
]