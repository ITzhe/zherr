from django.conf.urls import url
from saltstack.views import deploy_views

urlpatterns = [
    url(r'command/',deploy_views.Command),

]