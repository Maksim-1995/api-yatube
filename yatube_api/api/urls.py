from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import GroupViewSet, PostViewSet, CommentViewSet


router_v1 = DefaultRouter()
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register('posts', PostViewSet, basename='posts')

v1_urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(router_v1.urls)),
    path('posts/<int:post_id>/comments/',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='post-comments-list'
    ),
    path('posts/<int:post_id>/comments/<int:pk>/',
    CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }),
    name='post-comments-detail'
    ),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
