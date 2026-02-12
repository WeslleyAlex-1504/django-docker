from django.contrib import admin
from django.urls import include, path

from inventory.views import home_redirect

urlpatterns = [
    path('', home_redirect, name='home'),
    path('estoque/', include('inventory.urls')),
    path('admin/', admin.site.urls),
]
