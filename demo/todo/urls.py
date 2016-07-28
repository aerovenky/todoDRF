from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^label/$', views.getLabels),
    url(r'^label/(?P<pk>[0-9]+)/$', views.LabelDetail),
    url(r'^note/$', views.getNotes),
    url(r'^note/(?P<pk>[0-9]+)/$', views.NoteDetail),
    url(r'^note/(?P<pk>[0-9]+)/label/$', views.NoteLabel),
    url(r'^label/(?P<label_id>[0-9]+)/notes/$', views.NoteByLabel),
]
