from django.contrib import admin

from .models import Position, Candidate, Band, Subarea, Area

admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Band)
admin.site.register(Subarea)
admin.site.register(Area)
