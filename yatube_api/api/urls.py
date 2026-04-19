from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested.routers import NestedSimpleRouter

from .views import GroupViewSet, PostViewSet, CommentViewSet


router_v1 = DefaultRouter()
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('posts', PostViewSet, basename='posts')

posts_router = NestedSimpleRouter(router_v1, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

v1_urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(router_v1.urls)),
    path('', include(posts_router.urls)),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
