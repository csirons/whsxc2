

from django.db import models

import datetime
import re




# Create your models here.

GENDER_CHOICES = (
  ('M', 'Male'),
  ('F', 'Female'),
)

class MaleManager(models.Manager):
  def get_query_set(self):
    return super(MaleManager, self).get_query_set().filter(gender='M')

class FemaleManager(models.Manager):
  def get_query_set(self):
    return super(FemaleManager, self).get_query_set().filter(gender='F')
  
class Course(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(null=True,blank=True)
  directions = models.TextField(null=True,blank=True)
  address1 = models.CharField(max_length=255,null=True,blank=True)
  zip_code = models.PositiveIntegerField(null=True,blank=True)
  route_url = models.CharField('Route URL', max_length=255,null=True,blank=True)
  route = models.TextField(null=True,blank=True)

class RunnerManager(models.Manager):
  def by_year(self,year):
    from django.db import connection
    cursor = connection.cursor()
    sql = """
      SELECT rr.id, rr.name, rr.gender, rr.year
      FROM crosscountry_runner rr
      LEFT JOIN crosscountry_run r ON (rr.id = r.runner_id)
      WHERE datetime(r.occurred_at) > datetime('%s-01-01') AND datetime(r.occurred_at) < datetime('%s-12-31 23:59:59')
      GROUP BY rr.id
      ORDER BY rr.year, rr.gender, rr.name
    """ % (year, year)
    cursor.execute(sql)
    result_list = []
    for row in cursor.fetchall():
      p = self.model(id=row[0], name=row[1], gender=row[2], year=row[3])
      p.grade = p.year - int(year)
      result_list.append(p)
    return result_list



class Runner(models.Model):
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add = True)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  year = models.IntegerField()

  people = RunnerManager()
  men = MaleManager()
  women = FemaleManager()

  class Meta:
    ordering = ['name']

  class Admin:
    list_filter = ['year','gender']
    search_fields = ['name']

  def __unicode__(self):
    return "%s" % self.name

  def get_absolute_url(self):
    return	"/runners/%i/" % self.id

  def pr_course(self,course_id,date):
    return self.run_set.filter(course=course_id,occurred_at__lt=date).order_by('final_time')[:1]

  def pr(self,date):
    return self.run_set.filter(occurred_at__lt=date).order_by('final_time')[:1]

  def sb(self,date):
    return None
#		beginning_of_year = datetime.date(date.year, 1, 1)
#		return self.run_set.filter(occurred_at__gte=beginning_of_year).filter(occurred_at__lt=date).order_by('final_time')[:1]

  def get_absolute_urls(self):
    url = self.get_absolute_url()

    return [
      url,
      url+'organize-course/',
      url+'sort-split1/',
      url+'sort-split2/',
      url+'sort-split3/',
      url+'sort-final/',
      url+'sort-place/',
      url+'sort-points/',
    ]

  def season_average(self, year):
    season_runs = self.run_set.filter(occurred_at__year=year)
    average = 0
    for run in season_runs:
      average = average + run.final_time
    average = average / len(season_runs)
    return average


class MeetManager(models.Manager):
  def years(self):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT strftime('%%Y',occurred_at) FROM crosscountry_meet GROUP BY strftime('%%Y', occurred_at) ORDER BY occurred_at asc;")
    result_list = []
    for row in cursor.fetchall():
      result_list.append(row[0])
    return result_list
  def by_year(self,year):
    return super(MeetManager, self).get_query_set().filter(occurred_at=year)

class Meet(models.Model):
  name = models.CharField(max_length=255, blank=True)
  #course = models.ForeignKey(Course)
  occurred_at = models.DateTimeField('date')
  num_teams = models.IntegerField(null=True,blank=True)
  official_results_url = models.URLField(blank=True, null=True)
  summary = models.TextField(null=True,blank=True)

  team_place_female = models.IntegerField(null=True,editable=False)
  top_finish_female = models.IntegerField(null=True,editable=False)
  pack_time_female = models.IntegerField(null=True,editable=False)
  team_place_male = models.IntegerField(null=True,editable=False)
  top_finish_male = models.IntegerField(null=True,editable=False)
  pack_time_male = models.IntegerField(null=True,editable=False)

  objects = MeetManager()

  class Admin:
    list_display = ('name','course','team_place_female','team_place_male','top_finish_female','top_finish_male')

  class Meta:
    ordering = ['-occurred_at']

  def __unicode__(self):
    return u"%s (%s)" % (self.name, self.occurred_at.year)

  def get_absolute_url(self):
    return	"/meets/%i/" % self.id

  def sorted_races(self):
    return self.race_set.all()

  def past_tense(self):
    #now = datetime.datetime.now()
    now = datetime.datetime.now() - datetime.timedelta(hours=3)

    return self.occurred_at < now

  def year(self):
    return self.occurred_at.year

  #TODO if I change a date, update all denormalized info in races and runs
  def calc_races_info(self, save=False):
    races = self.race_set.filter(team__in=('1GV','2BV'))

    for race in races:
      if race.team == '1GV':
        self.team_place_female = race.team_place
        self.top_finish_female = race.top_finish
        self.pack_time_female = race.pack_time
      else:
        self.team_place_male = race.team_place
        self.top_finish_male = race.top_finish
        self.pack_time_male = race.pack_time

    if save:
      self.save()

  def get_absolute_urls(self):
    url = self.get_absolute_url()

    return [
      url,
      url+'sort-split1/',
      url+'sort-split2/',
      url+'sort-split3/',
      url+'sort-final/',
      url+'sort-place/',
      url+'sort-points/',
    ]