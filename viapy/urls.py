from django.conf.urls import url

from viapy.views import ViafLookup, ViafSearch


urlpatterns = [
    url(r'^suggest/$', ViafLookup.as_view(), name='suggest'),
    url(r'^suggest/person/$', ViafLookup.as_view(),
        {'nametype': 'personal'}, name='person-suggest'),
    url(r'^search/$', ViafSearch.as_view(), name='search'),
    url(r'^search/person/$', ViafSearch.as_view(),
        {'nametype': 'personal'}, name='person-search'),
]
