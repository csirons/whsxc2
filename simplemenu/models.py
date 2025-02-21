from django.db import models

# Create your models here.
class Menu(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()

	class Admin:
		pass

	def __unicode__(self):
		return "%s" % self.name

class MenuItem(models.Model):
	menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
	url = models.CharField(max_length=1024)
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=255,blank=True,null=True)
	sort = models.IntegerField(default=0)

	class Meta:
		ordering = ['sort']

	class Admin:
		pass

	def __unicode__(self):
		return "%s - %s - %s" % (self.menu.name, self.sort, self.title)

