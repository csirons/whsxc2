from django.db import models

# Create your models here.
class Entry(models.Model):
	title = models.CharField(max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	class Admin:
		pass

	def __str__(self):
		return "%s" % self.title
