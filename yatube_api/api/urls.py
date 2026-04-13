from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import GroupViewSet, PostViewSet


v1_router = DefaultRouter()
v1_router.register('groups', GroupViewSet, basename='groups')
v1_router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(v1_router.urls)),
]
