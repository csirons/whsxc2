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

    def save_model(self, request, race, form, change):
         super().save_model(request, race, form, change)

         # race = get_object_or_404(Race, pk=race_id)
         race.update_denormalized()
         race.calc_race_info()
         race.save()
         race.meet.calc_races_info(save=True)

         for run in race.run_set.all():
           run.update_denormalized()
           run.calc_personal_records()
           run.calc_letter_points()
           run.save()


@admin.register(Runner)
class RunnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'gender')
    #list_filter = ['team','occurred_at','course_name']
    list_filter = ['name', 'year', 'gender']
    js = [ '/media/javascript/convert_times.js' ]

    def save_model(self, request, race, form, change):
         super().save_model(request, race, form, change)

         for run in runner.run_set.order_by('id'):
           race = run.race
           race.update_denormalized()
           race.calc_race_info()
           race.save()

           run.meet.calc_races_info(save=True)

           run.update_denormalized()
           run.calc_personal_records()
           run.calc_letter_points()
           run.save()



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
