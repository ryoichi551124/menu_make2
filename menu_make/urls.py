from django.contrib import admin
from django.urls import path, include

from django.views.generic import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('menu.urls')),

    path('accounts/login/', base.RedirectView.as_view(pattern_name="login")),
    path('accounts/profile/', base.RedirectView.as_view(pattern_name="index")),
]
