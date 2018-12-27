from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index),
    #path('', views.test),
    #path('', views.test2),
    path('', views.index),
    #re_path(r'^$', views.IndexView.as_view(), name='index'),
    #re_path(r'^ajaxproject/$', views.ajaxproject, name='ajaxproject'),
    ]
