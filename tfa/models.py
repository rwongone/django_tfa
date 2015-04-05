from django.db import models

class User(models.Model):
	username = models.CharField(max_length=200, unique=True)
	password = models.CharField(max_length=200)
	tfaEnabled = models.BooleanField(default=True)
	tfaSecret = models.CharField(max_length=16)

	def __str__(self):
		return self.username
# Create your models here.
