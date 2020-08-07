from django.urls import include, path

from .views import setup, evaluation, review, conclusion, observations, template_upload

app_name = 'interview'
urlpatterns = [
    path('', setup, name='setup'),
    path('evaluation', evaluation, name='evaluation'),
    path('review', review, name='review'),
    path('conclusion', conclusion, name='conclusion'),
    path('observations', observations, name='observations'),
    path('template', template_upload, name='template_upload'),
]
