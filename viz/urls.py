from django.urls import include, path

from .views import detail

app_name = 'viz'
urlpatterns = [
    path('<int:interview_id>', detail, name='detail'),
]
