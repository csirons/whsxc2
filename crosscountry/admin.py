from django.contrib import admin
from crosscountry.models import Race


class RaceAdmin(admin.ModelAdmin):
    list_display = ('meet','team','course_name','team_place','top_finish','pack_time')
    list_filter = ['team','occurred_at','course_name']
    js = [ '/media/javascript/convert_times.js' ]


admin.site.register(Race, RaceAdmin)
