from django.conf.urls import patterns, url, include
from django.contrib import admin

from rest_framework import routers

from authentication.views import UserViewSet, LoginView, LogoutView

from .views import IndexView

from accounts.views import (
    AccountView, AccountsRecentlyUpdatedView, AccountsLeaderboardsView)
from heroes.views import (
    HeroView, HeroRecentlyUpdatedView, HeroLeaderboardsView)

router = routers.SimpleRouter()
router.register(r'register', UserViewSet, base_name='register')

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(router.urls)),

    url(r'^api/auth/login/?$', LoginView.as_view(), name='login'),
    url(r'^api/auth/logout/?$', LogoutView.as_view(), name='logout'),

    url(r'^api/accounts/?$', AccountView.as_view(), name='accounts-list'),
    url(r'^api/accounts/(?P<region>\w+)/(?P<battle_tag>\w{2,12}-\d{4})/?$',
        AccountView.as_view(), name='account-details'),
    url(r'^api/accounts/recent/?$', AccountsRecentlyUpdatedView.as_view(),
        name='accounts-recent'),
    url(r'^api/accounts/leaderboards/(?P<region>\w+)/(?P<league>\w+[-]*\w+)/?$',
        AccountsLeaderboardsView.as_view(), name='accounts-leaderboards'),

    url(r'^api/heroes/$', HeroView.as_view(), name='hero-list'),
    url(r'^api/heroes/(?P<region>\w+)/(?P<battle_tag>\w{2,12}-\d{4})/(?P<hero_id>\d+)/?$',
        HeroView.as_view(), name='hero-details'),
    url(r'^api/heroes/recent/?$', HeroRecentlyUpdatedView.as_view(),
        name='heroes-recent'),
    url(r'^api/heroes/leaderboards/(?P<region>\w+)/(?P<league>\w+[-]*\w+)/?$',
        HeroLeaderboardsView.as_view(), name='heroes-leaderboards'),

    url('^.*$', IndexView.as_view(), name='index'),
)
