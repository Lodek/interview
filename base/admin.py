from django.contrib import admin

from .models import Position, Candidate, Seniority, Subarea, Area


class SubareaInline(admin.TabularInline):
    model = Subarea
    extra = 1


class AreaAdmin(admin.ModelAdmin):
    inlines = [SubareaInline]


admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Seniority)
admin.site.register(Subarea)
admin.site.register(Area, AreaAdmin)
