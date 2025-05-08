from django.contrib import admin
from crosscountry.models import Race


class RaceAdmin(admin.ModelAdmin):
    list_display = ('meet','team','course_name','team_place','top_finish','pack_time')
    list_filter = ['team','occurred_at','course_name']
    js = [ '/media/javascript/convert_times.js' ]


admin.site.register(Race, RaceAdmin)



from django.contrib import admin
from crosscountry.models import Runner


class RunnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'gender')
    #list_filter = ['team','occurred_at','course_name']
    list_filter = ['name', 'year', 'gender']
    js = [ '/media/javascript/convert_times.js' ]



admin.site.register(Runner, RunnerAdmin)


from crosscountry.models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address1', 'zip_code', 'directions', 'description', 'route_url')
    list_filter = ['name']
    js = [ '/media/javascript/convert_times.js' ]



admin.site.register(Course, CourseAdmin)



from crosscountry.models import Meet


class MeetAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'name', 'occurred_at', 'num_teams', 'official_results_url', 'summary', 'team_place_female', 'top_finish_female', 'pack_time_female', 'team_place_male', 'top_finish_male', 'pack_time_male')
    list_filter = ['name']
    js = [ '/media/javascript/convert_times.js' ]



admin.site.register(Meet, MeetAdmin)