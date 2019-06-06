from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'start',views.start, name='start'),
    url(r'stop',views.stop, name='stop'),
    url(r'proto',views.proto_num, name='get_proto_num'),
]