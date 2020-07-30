from django.urls import include, path

from .views import detail, list

app_name = 'viz'
urlpatterns = [
    path('', list, name='list'),
    path('<int:interview_id>', detail, name='detail'),
]
