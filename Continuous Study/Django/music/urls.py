from django.conf.urls import url
from . import views


app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<album_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<album_id>\d+)/favorite/$', views.favorite, name='favorite')
]
