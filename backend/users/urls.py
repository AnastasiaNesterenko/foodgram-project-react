from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, FollowApiView, FollowListViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/users/subscriptions/',
         FollowListViewSet.as_view(),
         name='subscriptions'),
    path('v1/users/<int:user_id>/subscribe/',
         FollowApiView.as_view(),
         name='subscribe'),
    path('v1/', include(router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
