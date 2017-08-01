"""Test URL configuration for viapy
"""
from django.conf.urls import url, include

from viapy import urls as viapy_urls


urlpatterns = [
    url(r'^viaf/', include(viapy_urls, namespace='viaf')),
]

