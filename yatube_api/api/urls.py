from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import views as token_views

from .views import GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', token_views.obtain_auth_token, name=' obtain_auth_token')
]
