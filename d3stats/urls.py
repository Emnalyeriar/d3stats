from django.conf.urls import patterns, url, include
from rest_framework import routers

from authentication.views import UserViewSet, LoginView, LogoutView
from .views import IndexView

router = routers.SimpleRouter()
router.register(r'accounts', UserViewSet)
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
    url('^.*$', IndexView.as_view(), name='index'),
)
