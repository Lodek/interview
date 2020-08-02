from django.contrib import admin

from .models import Question, Template, Interview, Score

admin.site.register(Question)
admin.site.register(Interview)
admin.site.register(Score)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    filter_vertical = ['questions']


