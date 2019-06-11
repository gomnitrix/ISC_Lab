from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'home', views.get_html, name='html'),
    url(r'start', views.start, name='start'),
    url(r'stop', views.stop, name='stop'),
    url(r'proto', views.proto_num, name='get_proto_num'),
    url(r'app', views.app_num, name='get_app_num'),
    url(r'pkt_sum', views.pkt_sum, name='sum'),
    url(r'riskflow', views.get_riskflow, name='riskflow'),
    url(r'get_rst_num', views.get_rst, name='rst_num'),
    url(r'dtl', views.riskflow_dtl, name='riskflow_dtl'),
    url(r'setting', views.get_setting, name='setting'),
    url(r'submit', views.filter, name='submit'),
    url(r'delete', views.filter_delete, name='delete'),
    url(r'block', views.get_block, name='block'),
]
