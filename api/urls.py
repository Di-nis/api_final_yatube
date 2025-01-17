from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CommentViewSet, FollowCreateListView, GroupCreateListView,
                    PostViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'posts/(?P<id>\d+)/comments', CommentViewSet, 'Comment')
router_v1.register(r'follow', FollowCreateListView)
router_v1.register(r'group', GroupCreateListView)


urlpatterns = [
        path('v1/token/',
             TokenObtainPairView.as_view(),
             name='token_obtain_pair'),
        path('v1/token/refresh/',
             TokenRefreshView.as_view(),
             name='token_refresh'),
        path('v1/', include(router_v1.urls)),
    ]
