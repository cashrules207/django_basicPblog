from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from django.core.urlresolvers import reverse

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length = 120)
	image = models.ImageField(null=True, blank= True, 
		width_field="width_field", #Filefield cannnot use the hieght and width field
		height_field="height_field") #when using the ImageField you must install Pillow.. pip install pillow
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False) #when it is edited/saved to the database
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) # when it is added to the database initially


	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs = {"id": self.id})

	class Meta:
		ordering= ["-timestamp", "-updated"]

# Create your models here.
