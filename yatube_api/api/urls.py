from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, PostViewSet, CommentViewSet


router = DefaultRouter()
router.register('groups', GroupViewSet)
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'posts/<int:post_id>/comments/',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='post-comments-list'
    ),
    path(
        'posts/<int:post_id>/comments/<int:pk>/',
        CommentViewSet.as_view({
            'get': 'retrieve',
            'put': 'update', 'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='post-comments-detail'
    ),
]
