from django.db import models

from apps.users.models import User
# Create your models here.



class Book(models.Model):

	title = models.CharField(max_length=255, unique=True)
	summary = models.TextField()

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


class Review(models.Model):
	
	user = models.ForeignKey(User)
	book = models.ForeignKey(Book)

	subject = models.CharField(max_length=255)
	comment = models.TextField()

	rating = models.IntegerField(default=0)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

class Author(models.Model):

	books = models.ManyToManyField(Book)

	name = models.CharField(max_length=255, unique=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)



	def __str__(self):
		return self.name