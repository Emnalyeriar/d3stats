from django.conf.urls import patterns, url, include
from rest_framework import routers

from authentication.views import UserViewSet, LoginView, LogoutView
from .views import IndexView

from accounts.views import AccountView, RecentlyUpdatedView

router = routers.SimpleRouter()
# router.register(r'accounts', AccountView, base_name='accounts')
# router.register(r'posts', PostViewSet)

# accounts_router = routers.NestedSimpleRouter(
#     router, r'accounts', lookup='account'
# )
# accounts_router.register(r'posts', AccountPostsViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    # url(r'^api/v1/', include(accounts_router.urls)),
    url(r'^api/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/auth/logout/$', LogoutView.as_view(), name='logout'),

    url(r'^api/accounts/$', AccountView.as_view(), name='accounts'),
    url(r'^api/accounts/(?P<region>\w+)/(?P<battle_tag>\w{2,12}-\d{4})/$',
        AccountView.as_view()),
    url(r'^api/accounts/recent/$', RecentlyUpdatedView.as_view(),
        name='recent'),
    url('^.*$', IndexView.as_view(), name='index'),
)
