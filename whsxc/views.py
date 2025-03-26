from django.http import HttpResponsePermanentRedirect
from django.views.generic import TemplateView # direct_to_template is deprecated, use TemplateView instead
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from blog.models import Entry
from crosscountry.models import *
import datetime


def homepage(request):
    # return HttpResponse("Hello, world. You're at homepage.")
    return render(request, 'home.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #"date_list": Entry.objects.years()
        },)

def archive(request):
    return render(request, "blog/entry_archive.html",  {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #"date_list": Entry.objects.all().order_by("-created_at"),
        },)

def runners(request):
    #def runners_list(request):
    # calculate which years have runners
    years = Meet.objects.years()
    actual_years = []
    runners_by_year = {}
    for year in years:
        runners = Runner.people.by_year(year)
        if len(runners) > 0:
            runners_by_year[year] = runners
            actual_years.append(year)

    return render(request,'runners/runners.html', {
        "runners_by_year": runners_by_year,  # Sort years in descending order
        "years": actual_years,
         },)


def meets(request):
    now = datetime.datetime.now()
    meets = Meet.objects.all().filter(occurred_at__lte=now).select_related().order_by('-occurred_at')    
    #print("meets: ", meets[:5])  # Debugging line to check the first 5 meets
    return render(request, 'meets/meets.html', {
        "meets": meets, 
        },)

def meet_detail(request, object_id=-1, sort=None):
#def meet_detail(request):
    #return render(request, 'history/history.html', {
    #        "latest": Entry.objects.all().order_by("-created_at")[:5],
    #        #datelist:
    #    },)

    meet = get_object_or_404(Meet, pk=object_id)
    races = meet.race_set.order_by('team')

    if sort == 'final':
        return HttpResponsePermanentRedirect(meet.get_absolute_url())

    if sort == None:
        sort = 'final'

    sort_field = {
    'split1': 'mile_1_time',
    'split2': 'split_2',
    'split3': 'split_3',
    'final': 'final_time',
    'place': 'place',
    'points': 'letter_points',
    }[sort]

    return render(request, 'meets/meet_detail.html', { 'meet': meet, 'races': races, 'sort_runs_by': sort_field,},)

def history(request):
    return render(request, 'history/history.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def schedule(request):
    return render(request, 'schedule/schedule.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def homemeet(request):
    return render(request, 'homemeet/homemeet.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def runninglinks(request):
    return render(request, 'runninglinks/runninglinks.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def summerrunning(request):
    return render(request, 'summerrunning/summerrunning.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

def courses_list(request):
  courses = Course.objects.all()
  return render(request, 'courses_list.html', { 'courses': courses })

def course_detail(request, object_id = -1, sort = 'final'):
    course = get_object_or_404(Course, pk=object_id)
    now = datetime.datetime.now()
    meets = course.meet_set.filter(occurred_at__lte=now)

    best_runs_male = Run.objects.select_related().filter(gender='M').filter(course=course).order_by('final_time')[:10]
    best_runs_female = Run.objects.select_related().filter(gender='F').filter(course=course).order_by('final_time')[:10]

    freshman_runs_male = Run.freshmanruns.filter(gender='M').filter(course=course).order_by('final_time')[:10]
    freshman_runs_female = Run.freshmanruns.filter(gender='F').filter(course=course).order_by('final_time')[:10]

    sophomore_runs_male = Run.sophomoreruns.filter(gender='M').filter(course=course).order_by('final_time')[:10]
    sophomore_runs_female = Run.sophomoreruns.filter(gender='F').filter(course=course).order_by('final_time')[:10]

    junior_runs_male = Run.juniorruns.filter(gender='M').filter(course=course).order_by('final_time')[:10]
    junior_runs_female = Run.juniorruns.filter(gender='F').filter(course=course).order_by('final_time')[:10]

    senior_runs_male = Run.seniorruns.filter(gender='M').filter(course=course).order_by('final_time')[:10]
    senior_runs_female = Run.seniorruns.filter(gender='F').filter(course=course).order_by('final_time')[:10]
    #return render(request, 'summerrunning/summerrunning.html', {
    #        "latest": Entry.objects.all().order_by("-created_at")[:5],
    #        #datelist:
    #    },)
    return render(request, 'course_detail.html', {
        'course': course,
        'best_runs_male': best_runs_male,
        'best_runs_female': best_runs_female,
        'freshman_runs_male': freshman_runs_male,
        'freshman_runs_female': freshman_runs_female,
        'sophomore_runs_male': sophomore_runs_male,
        'sophomore_runs_female': sophomore_runs_female,
        'junior_runs_male': junior_runs_male,
        'junior_runs_female': junior_runs_female,
        'senior_runs_male': senior_runs_male,
        'senior_runs_female': senior_runs_female,
        'meets': meets,
        },)

def top10_list(request):
    best_runners_male = Run.objects.filter(gender='M').extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).order_by('best_time').distinct('runner_id')[:10]
    #best_runners_male = Run.objects.filter(gender='M').extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).order_by('best_time')#.group_by('runner_id')[:10]
    best_runners_female = Run.objects.extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).filter(gender='F').order_by('best_time').distinct('runner_id')[:10]

    freshman_runners_male = Run.freshmanruns.filter(gender='M').extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).order_by('best_time').distinct('runner_id')[:10]
    freshman_runners_female = Run.freshmanruns.extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).filter(gender='F').order_by('best_time').distinct('runner_id')[:10]
    sophomore_runners_male = Run.sophomoreruns.filter(gender='M').extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).order_by('best_time').distinct('runner_id')[:10]
    sophomore_runners_female = Run.sophomoreruns.extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).filter(gender='F').order_by('best_time').distinct('runner_id')[:10]
    junior_runners_male = Run.juniorruns.filter(gender='M').extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).order_by('best_time').distinct('runner_id')[:10]
    junior_runners_female = Run.juniorruns.extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).filter(gender='F').order_by('best_time').distinct('runner_id')[:10]
    senior_runners_male = Run.seniorruns.filter(gender='M').extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).order_by('best_time').distinct('runner_id')[:10]
    senior_runners_female = Run.seniorruns.extra(select={'best_time': 'MIN("crosscountry_run"."final_time")'}).filter(gender='F').order_by('best_time').distinct('runner_id')[:10]

    best_runs_male = Run.objects.select_related().filter(gender='M').order_by('final_time')[:10]
    best_runs_female = Run.objects.select_related().filter(gender='F').order_by('final_time')[:10]

    freshman_runs_male = Run.freshmanruns.filter(gender='M').order_by('final_time')[:10]
    freshman_runs_female = Run.freshmanruns.filter(gender='F').order_by('final_time')[:10]

    sophomore_runs_male = Run.sophomoreruns.filter(gender='M').order_by('final_time')[:10]
    sophomore_runs_female = Run.sophomoreruns.filter(gender='F').order_by('final_time')[:10]

    junior_runs_male = Run.juniorruns.filter(gender='M').order_by('final_time')[:10]
    junior_runs_female = Run.juniorruns.filter(gender='F').order_by('final_time')[:10]

    senior_runs_male = Run.seniorruns.filter(gender='M').order_by('final_time')[:10]
    senior_runs_female = Run.seniorruns.filter(gender='F').order_by('final_time')[:10]

    #return render(request, 'summerrunning/summerrunning.html', {
    #        "latest": Entry.objects.all().order_by("-created_at")[:5],
    #        #datelist:
    #    },)

    return render(request,'runners/top10_list.html', {
        'best_runners_male': best_runners_male,
        'best_runners_female': best_runners_female,
        'freshman_runners_male': freshman_runners_male,
        'freshman_runners_female': freshman_runners_female,
        'sophomore_runners_male': sophomore_runners_male,
        'sophomore_runners_female': sophomore_runners_female,
        'junior_runners_male': junior_runners_male,
        'junior_runners_female': junior_runners_female,
        'senior_runners_male': senior_runners_male,
        'senior_runners_female': senior_runners_female,
        'best_runs_male': best_runs_male,
        'best_runs_female': best_runs_female,
        'freshman_runs_male': freshman_runs_male,
        'freshman_runs_female': freshman_runs_female,
        'sophomore_runs_male': sophomore_runs_male,
        'sophomore_runs_female': sophomore_runs_female,
        'junior_runs_male': junior_runs_male,
        'junior_runs_female': junior_runs_female,
        'senior_runs_male': senior_runs_male,
        'senior_runs_female': senior_runs_female,
        },)

def runner_detail(request, object_id=-1, sort=None, organize="year"):
  # calculate which years has been running
  # calculate letter points for those years using a group by and SUM

  runner = get_object_or_404(Runner, pk=object_id)

  if sort == 'date':
    return HttpResponsePermanentRedirect(runner.get_absolute_url())

  if sort == None:
    sort = 'date'

  sort_field = {
    'split1': 'mile_1_time',
    'split2': 'split_2',
    'split3': 'split_3',
    'final': 'final_time',
    'place': 'place',
    'points': 'letter_points',
    'date': '-occurred_at',
  }[sort]

  if not organize:
    organize = 'year'

  organize_field = {
    'year': 'year',
    'course': 'course',
  }[organize]

  organize_direction = {
    'year': '-',
    'course': '',
  }[organize]

  runs = runner.run_set.extra(select={'year': 'strftime("%%Y",occurred_at)'}).order_by(organize_direction+organize_field,sort_field)
 
  #return render(request, 'summerrunning/summerrunning.html', {
  #          "latest": Entry.objects.all().order_by("-created_at")[:5],
  #          #datelist:
  #      },)


  return render(request,'runners/runner_detail.html', { 'runner':runner, 'runs':runs, 'sort_runs_by':sort_field, 'organize_field':organize_field },)

