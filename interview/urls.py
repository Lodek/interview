from django.urls import include, path

from .views import setup, evaluation

app_name = 'interview'
urlpatterns = [
    path('', setup),
    path('evaluation', evaluation),
]
