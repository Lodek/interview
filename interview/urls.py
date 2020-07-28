from django.urls import include, path

from .views import setup, evaluation, review, conclusion

app_name = 'interview'
urlpatterns = [
    path('', setup, name='setup'),
    path('evaluation', evaluation, name='evaluation'),
    path('review', review, name='review'),
    path('conclusion', conclusion, name='conclusion'),
]
