from django.db import models
from django.contrib.admin import TabularInline
from django.dispatch import dispatcher
from django.db.models import signals
#from crosscountry import signals as mysignals

#import urllib2 # thi s is for version 2.x
import urllib # this is for version 3.x
import datetime
import re

#import route_url_lib

route_urls = {
  #http://runkeeper.com/user/315746892/activity/56941773
  r'https?:\/\/runkeeper.com\/user\/[0-9]+\/activity\/[0-9]+': lambda url: route_url_lib.runkeeper(url),
}
# Create your models here.

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

class MaleManager(models.Manager):
  def get_query_set(self):
    return super(MaleManager, self).get_query_set().filter(gender='M')

class FemaleManager(models.Manager):
  def get_query_set(self):
    return super(FemaleManager, self).get_query_set().filter(gender='F')

GENDER_CHOICES = (
  ('M', 'Male'),
  ('F', 'Female'),
)

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

class Course(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(null=True,blank=True)
  directions = models.TextField(null=True,blank=True)
  address1 = models.CharField(max_length=255,null=True,blank=True)
  zip_code = models.PositiveIntegerField(null=True,blank=True)
  route_url = models.CharField('Route URL', max_length=255,null=True,blank=True)
  route = models.TextField(null=True,blank=True)

  class Meta:
    ordering = ['name']

  class Admin:
    list_display = ('name','address1','zip_code')

  def __unicode__(self):
    return self.name

  def get_absolute_url(self):
    return	"/courses/%i/" % self.id

  def save(self):
    if not self.route and self.route_url:
      for r in route_urls:
        p = re.compile(r)
        if p.match(self.route_url):
          self.route = route_urls[r](self.route_url)

    super(Course, self).save()

class MeetManager(models.Manager):
  def years(self):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT strftime('%Y',occurred_at) FROM crosscountry_meet GROUP BY strftime('%Y', occurred_at) ORDER BY occurred_at asc;")
    result_list = []
    for row in cursor.fetchall():
      result_list.append(row[0])
    return result_list
  def by_year(self,year):
    return super(MeetManager, self).get_query_set().filter(occurred_at=year)

class Meet(models.Model):
  name = models.CharField(max_length=255, blank=True)
  course = models.ForeignKey(Course,on_delete=models.SET_NULL, null=True, blank=True) # course can be null for meets that are not on a specific course on_delete=models.CASCADE,
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
    db_table = 'crosscountry_meet'
    ordering = ['-occurred_at']
  

  def __str__(self):
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

TEAM_CHOICES = (
    ('1GV', 'Girls Varsity'),
    ('2BV', 'Boys Varsity'),
    ('3GJ', 'Girls JV'),
    ('4BJ', 'Boys JV'),
    ('5GF', 'Girls Frosh/Soph'),
    ('6BF', 'Boys Frosh/Soph'),
)
TEAM_CHOICES_REVERSE = {
    '1GV': 'Girls Varsity',
    '2BV': 'Boys Varsity',
    '3GJ': 'Girls JV',
    '4BJ': 'Boys JV',
    '5GF': 'Girls Frosh/Soph',
    '6BF': 'Boys Frosh/Soph',
}

class Race(models.Model):
  meet = models.ForeignKey(Meet,on_delete=models.SET_NULL, null=True, blank=True)
  team = models.CharField(max_length=3, choices=TEAM_CHOICES)
  time = models.TimeField(null=True,blank=True)
  num_runners = models.IntegerField(null=True,blank=True)
  team_place = models.IntegerField(null=True,blank=True)
  num_teams = models.IntegerField(null=True,blank=True)

  #updated automagically
  top_finish = models.IntegerField(null=True,editable=False)
  pack_time = models.IntegerField(null=True,editable=False)

  #denormalizing info
  meet_name = models.CharField(max_length=255, editable=False)
  course_name = models.CharField(max_length=255,editable=False)
  occurred_at = models.DateTimeField('date',editable=False)

  def save(self):
    self.course_name = self.meet.course.name
    self.occurred_at = self.meet.occurred_at
    self.meet_name = "%s" % self.meet

    super(Race,self).save()

  class Admin:
    list_display = ('meet','team','course_name','team_place','top_finish','pack_time')
    list_filter = ['team','occurred_at','course_name']
    date_hierarchy = 'occurred_at'
    js = [ '/media/javascript/convert_times.js' ]

  def __unicode__(self):
    return "%s - %s" % (self.meet_name, TEAM_CHOICES_REVERSE[self.team])

  def sorted_runs(self):
    return self.run_set.order_by('final_time')

  def update_denormalized(self, save=False):
    pass

  def calc_race_info(self, save=False):
    runs = self.run_set.order_by('final_time')

    self.top_finish = None
    for run in runs:
      if run.place:
        self.top_finish = run.place
        break

    if len(runs) < 2:
      self.pack_time = None
    else:
      self.pack_time = runs[len(runs)-1].final_time - runs[0].final_time

    if save:
      self.save()

class FreshmanRunsManager(models.Manager):
  def get_query_set(self):
    return super(FreshmanRunsManager, self).get_query_set().filter(grade=4).order_by('final_time')

class SophomoreRunsManager(models.Manager):
  def get_query_set(self):
    return super(SophomoreRunsManager, self).get_query_set().extra(tables=['crosscountry_runner'],where=['crosscountry_runner.id = crosscountry_run.runner_id',("(crosscountry_runner.year - strftime('%%Y',crosscountry_run.occurred_at)) = 3")]).order_by('final_time')

class JuniorRunsManager(models.Manager):
  def get_query_set(self):
    return super(JuniorRunsManager, self).get_query_set().extra(tables=['crosscountry_runner'],where=['crosscountry_runner.id = crosscountry_run.runner_id',("(crosscountry_runner.year - strftime('%%Y',crosscountry_run.occurred_at)) = 2")]).order_by('final_time')

class SeniorRunsManager(models.Manager):
  def get_query_set(self):
    return super(SeniorRunsManager, self).get_query_set().extra(tables=['crosscountry_runner'],where=['crosscountry_runner.id = crosscountry_run.runner_id',("(crosscountry_runner.year - strftime('%%Y',crosscountry_run.occurred_at)) = 1")]).order_by('final_time')

class Run(models.Model):
  #runner = models.ForeignKey(Runner, edit_inline=models.TABULAR)
  #race = models.ForeignKey(Race, edit_inline=models.TABULAR, min_num_in_admin=7)
  runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
  race = models.ForeignKey(Race, on_delete=models.CASCADE)
  mile_1_time = models.IntegerField(null=True,blank=True)
  mile_2_time = models.IntegerField(null=True,blank=True)
  split_2 = models.IntegerField(null=True,editable=False)
  split_3 = models.IntegerField(null=True,editable=False)
  #final_time = models.IntegerField(core=True)
  final_time = models.IntegerField(null=True,blank=True) # in seconds
  place = models.IntegerField(null=True,blank=True)

  # calculate automagically
  letter_points = models.IntegerField(null=True,editable=False)
  pr = models.BooleanField(editable=False)
  pr_course = models.BooleanField(editable=False)
  sb = models.BooleanField(editable=False)
  all_time_rank = models.IntegerField(editable=False)
  grade_rank = models.IntegerField(editable=False)
  course_rank = models.IntegerField(editable=False)

  # denormalizing info
  gender = models.CharField(max_length=1,editable=False)
  meet = models.ForeignKey(Meet,editable=False, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, editable=False, on_delete=models.CASCADE)
  occurred_at = models.DateTimeField('date', editable=False)
  grade = models.IntegerField(editable=False)

  # managers
  objects = models.Manager()
  freshmanruns = FreshmanRunsManager()
  sophomoreruns = SophomoreRunsManager()
  juniorruns = JuniorRunsManager()
  seniorruns = SeniorRunsManager()

  class Admin:
    pass

  def __unicode__(self):
    return "Run for %s" % self.runner.name

  def calc_letter_points(self):
    points = 0

    if self.race.team.find('V') >= 0:
      points = points + 15

      if self.place and self.place <= 15:
        points = points + 50

      if self.place and self.place == 1:
          points = points + 50

      if self.place and self.race.num_runners:
        place_percent = (1.*self.place)/self.race.num_runners
        if self.place == 1:
          points = points + 0
        elif place_percent < 0.1:
          points = points + 20
        elif place_percent < 0.2:
          points = points + 15
        elif place_percent < 0.3:
          points = points + 10
        elif place_percent < 0.4:
          points = points + 5
        elif place_percent < 0.5:
          points = points + 3

      meet_place = None
      if self.gender == 'M':
        meet_place = self.meet.team_place_male
      else:
        meet_place = self.meet.team_place_female

      if meet_place:
        if meet_place == 1:
          points = points + 50
        elif meet_place == 2:
          points = points + 20
        elif meet_place == 3:
          points = points + 10
        elif meet_place == 4:
          points = points + 5

    elif self.race.team.find('J') >= 0:
      points = points + 5
      if self.place and self.race.num_runners:
        place_percent = (1.*self.place)/self.race.num_runners
        if self.place == 1:
          points = points + 20
        elif place_percent < 0.1:
          points = points + 15
        elif place_percent < 0.2:
          points = points + 10
        elif place_percent < 0.3:
          points = points + 5
        elif place_percent < 0.4:
          points = points + 3

    if self.pr_course:
      points = points + 10
    elif self.pr:
      points = points + 5

    self.letter_points = points

  def update_denormalized(self, save=False):
    pass

  def calc_rankings(self):
    self.all_time_rank = Run.objects.filter(gender=self.gender).filter(final_time__lt=self.final_time).count()+1
    self.course_rank = Run.objects.filter(gender=self.gender).filter(course=self.course).filter(final_time__lt=self.final_time).count()+1
    self.grade_rank = Run.objects.filter(gender=self.gender).filter(grade=self.grade).filter(final_time__lt=self.final_time).count()+1

  def save(self):
    self.gender = self.runner.gender
    self.meet = self.race.meet
    self.course = self.meet.course
    self.occurred_at = self.meet.occurred_at
    self.grade = self.runner.year - self.occurred_at.year

    self.calc_rankings()

    if self.mile_1_time and self.mile_2_time:
      self.split_2 = self.mile_2_time - self.mile_1_time
    if self.mile_2_time:
      self.split_3 = self.final_time - self.mile_2_time

    self.calc_letter_points()

    super(Run,self).save()

  def calc_personal_records(self, save=False):
    pr_course = self.runner.pr_course(self.course_id, self.occurred_at)
    if pr_course and self.final_time < pr_course[0].final_time:
      self.pr_course = True
    else:
      self.pr_course = False

    pr = self.runner.pr(self.occurred_at)
    if pr and self.final_time < pr[0].final_time:
      self.pr = True
    else:
      self.pr = False

    sb = self.runner.sb(self.occurred_at)
    if sb and self.final_time < sb[0].final_time:
      self.sb = True
    else:
      self.sb = False

    if save:
      self.save()

  def mile_3_pace(self):
    return (self.split_3)*(1./1782)*1609

  def year(self):
    return self.occurred_at.year

