from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from server.views import (
    OffersPage,
    check_subscription,
    log_js,
    show_friends,
    show_leaderboard,
    show_offers,
)

urlpatterns = [
    path("", OffersPage.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("check_subscription/", check_subscription, name="check_subscription"),
    path("show_offers/", show_offers, name="show_offers"),
    path("show_leaderboard/", show_leaderboard, name="show_leaderboard"),
    path("show_friends/", show_friends, name="show_friends"),
    path("log_js/", log_js, name="log_js"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
