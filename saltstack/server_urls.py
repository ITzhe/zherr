from django.conf.urls import url
from saltstack.views import server_views

urlpatterns = [
    url(r'add/$',server_views.server_add),
    url(r'list/$',server_views.server_list),
    url(r'del/(?P<id>\d+)/$',server_views.server_del),
    url(r'list/info/(?P<id>\d+)/$',server_views.server_info),
    url(r'room_info_edit/(?P<id>\d+)/$', server_views.room_edit),
    url(r'network_info_edit/(?P<id>\d+)/$', server_views.network_edit),
    url(r'index/$', server_views.index),
    url(r'default/$', server_views.default),
    url(r'status/$', server_views.server_status),
]