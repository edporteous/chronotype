from django.conf.urls import patterns, url

from quiz import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^results/$', views.results, name='results'),
    url(r'^printbadge/$', views.printbadge, name='printbadge'),
)