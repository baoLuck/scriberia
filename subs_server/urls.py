"""
URL configuration for subs_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from server.views import OffersPage, check_subscription, show_offers, log_js, show_leaderboard, show_friends
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', OffersPage.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('check_subscription/', check_subscription, name='check_subscription'),
    path('show_offers/', show_offers, name='show_offers'),
    path('show_leaderboard/', show_leaderboard, name='show_leaderboard'),
    path('show_friends/', show_friends, name='show_friends'),
    path('log_js/', log_js, name='log_js'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
