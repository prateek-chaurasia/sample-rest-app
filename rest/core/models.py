from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for items in LEXERS])
STYLE_CHOICES = sorted((item,item) for item in get_all_styles())

# Create your models here.
class Snippet(models.Model):
	"""
		This model calss represents the db schema for Snippet table.
	"""
	created = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, related_name='snippets', on_delete=models.CASCADE)
	title = models.CharField(max_length=100, blank=True, default='')
	code = models.TextField()
	linenos = models.BooleanField(default=False)
	highlighted = models.TextField()
	language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
	style = models.CharField(choices=STYLE_CHOICES, default='fiendly', max_length=100)
	
	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		"""
		Use the `pygments` library to create a highlighted HTML
    	representation of the code snippet.
    	"""
		lexer = get_lexer_by_name(self.language)
		linenos = self.linenos and 'table' or False
		options = self.title and {'title': self.title} or {}
		formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
		self.highlighted = highlight(self.code, lexer, formatter)
		super(Snippet, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	"""
		This is a signal method which recieves the signal whenever a 
		new user is saved in the database. As soon as it gets the 
		signal it gets executed.
	"""
	if created:
		Token.objects.create(user=instance)

