from django.http import HttpResponsePermanentRedirect
from django.views.generic import TemplateView # direct_to_template is deprecated, use TemplateView instead
from django.shortcuts import render
from blog.models import Entry
from crosscountry.models import *


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
    return render(request, 'history/history.html', {
            "latest": Entry.objects.all().order_by("-created_at")[:5],
            #datelist:
        },)

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

    return redender(request, 'meets/meet_detail.html', { 'meet': meet, 'races': races, 'sort_runs_by': sort_field,},)

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