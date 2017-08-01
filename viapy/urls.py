from django.conf.urls import url

from viapy.views import ViafLookup


urlpatterns = [
    url(r'^suggest/$', ViafLookup.as_view(), name='lookup'),
    url(r'^suggest/person/$', ViafLookup.as_view(),
        {'nametype': 'personal'}, name='person-lookup'),
]
