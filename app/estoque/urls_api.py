from django.urls import path

from .views import FrutaApiView

urlpatterns = [
    path('frutas/', FrutaApiView.as_view(), name='frutas-api'),
]
