from django.urls import include, path

from .views import detail

app_name = 'viz'
urlpatterns = [
    path('<int:pk>', detail, name='detail'),
]
