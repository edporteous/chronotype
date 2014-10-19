from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^printbadge/$', views.printbadge, name='printbadge'),
)