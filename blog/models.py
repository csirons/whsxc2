from django.db import models

# Create your models here.

class EntryManager(models.Manager):
  def years(self):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT strftime('%Y',created_at) FROM blog_entry GROUP BY strftime('%Y', created_at) ORDER BY created_at asc;")
    result_list = []
    for row in cursor.fetchall():
      result_list.append(row[0])
    return result_list


class Entry(models.Model):
	title = models.CharField(max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	objects = EntryManager()

	class Admin:
		pass

	def __unicode__(self):
		return "%s" % self.title

	def Meta(self):
		ordering = ['-created_at']
		db_table = 'blog_entry'
