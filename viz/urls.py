from django.urls import include, path

from .views import detail, list, compare

app_name = 'viz'
urlpatterns = [
    path('', list, name='list'),
    path('<int:interview_id>', detail, name='detail'),
    path('compare', compare, name='compare'),
]
