from django.contrib import admin
from crosscountry.models import Race, Runner, Course, Meet, Run


class RunInline(admin.TabularInline):
    model = Run
    extra = 5

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('meet','team','course_name','team_place','top_finish','pack_time')
    list_filter = ['team','occurred_at','course_name']
    js = [ '/media/javascript/convert_times.js' ]
    inlines = [RunInline]


@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'gender')
    #list_filter = ['team','occurred_at','course_name']
    list_filter = ['name', 'year', 'gender']
    js = [ '/media/javascript/convert_times.js' ]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','route_url')
    list_filter = ['name']
    js = [ '/media/javascript/convert_times.js' ]


@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    list_display = ('name', 'occurred_at')
    list_filter = ['name']
    js = [ '/media/javascript/convert_times.js' ]

@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    js = [ '/media/javascript/convert_times.js' ]
