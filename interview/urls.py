from django.urls import include, path

from .views import setup, evaluation, review

app_name = 'interview'
urlpatterns = [
    path('', setup),
    path('evaluation', evaluation),
    path('review', review),
]
