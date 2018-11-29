from django.db import models

# Create your models here.
class User(models.Model):
	uname = models.TextField()

class Snippet(models.Model):
	uploadUser = models.TextField()
	editedBy = models.TextField()
	title = models.TextField()
	language = models.TextField()
	originalSnippet = models.TextField()
	editedSnippet = models.TextField()