from django.urls import include, path

from .views import detail, list, compare, json_export

app_name = 'viz'
urlpatterns = [
    path('', list, name='list'),
    path('<int:interview_id>', detail, name='detail'),
    path('<int:interview_id>/json', json_export, name='json'),
    path('compare', compare, name='compare'),
]
