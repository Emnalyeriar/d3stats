from django.conf.urls import patterns, url, include
from django.contrib import admin

from rest_framework import routers

from authentication.views import UserViewSet, LoginView, LogoutView

from .views import IndexView

from accounts.views import AccountView, RecentlyUpdatedView, LeaderboardsView
from heroes.views import HeroView

router = routers.SimpleRouter()
router.register(r'register', UserViewSet, base_name='register')

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(router.urls)),

    url(r'^api/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/auth/logout/$', LogoutView.as_view(), name='logout'),

    url(r'^api/accounts/$', AccountView.as_view(), name='accounts-list'),
    url(r'^api/accounts/(?P<region>\w+)/(?P<battle_tag>\w{2,12}-\d{4})/$',
        AccountView.as_view(), name='account-details'),
    url(r'^api/accounts/recent/$', RecentlyUpdatedView.as_view(),
        name='recent'),
    url(r'^api/accounts/leaderboards/(?P<region>\w+)/(?P<league>\w+[-]*\w+)/$',
        LeaderboardsView.as_view(), name='leaderboards'),

    url(r'^api/heroes/$', HeroView.as_view(), name='accounts-list'),

    url('^.*$', IndexView.as_view(), name='index'),
)
