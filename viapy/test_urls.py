"""Test URL configuration for viapy
"""
try:
    from django.urls import path, include

    from viapy import urls as viapy_urls

    urlpatterns = [
        path(r"viaf/", include(viapy_urls, namespace="viaf")),
    ]

except ImportError:
    pass
