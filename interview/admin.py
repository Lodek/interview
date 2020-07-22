from django.contrib import admin

from .models import Question, Template, Interview, Score

admin.site.register(Question)
admin.site.register(Template)
admin.site.register(Interview)
admin.site.register(Score)
