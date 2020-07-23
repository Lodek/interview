from django.urls import include, path

from .views import setup

app_name = 'interview'
urlpatterns = [
    path('', setup),
]
