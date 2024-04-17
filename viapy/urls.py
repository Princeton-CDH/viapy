from django.urls import path

from viapy.views import ViafLookup, ViafSearch


app_name = "viapy"

urlpatterns = [
    path("suggest/", ViafLookup.as_view(), name="suggest"),
    path(
        "suggest/person/",
        ViafLookup.as_view(),
        {"nametype": "personal"},
        name="person-suggest",
    ),
    path("search/", ViafSearch.as_view(), name="search"),
    path(
        "search/person/",
        ViafSearch.as_view(),
        {"nametype": "personal"},
        name="person-search",
    ),
]
