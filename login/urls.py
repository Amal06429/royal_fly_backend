from django.urls import path
from .views import LoginAPIView, TokenRefreshAPIView, UsersAPIView, UserDetailAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshAPIView.as_view(), name='token-refresh'),
    path('users/', UsersAPIView.as_view(), name='users-list'),
    path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='users-detail'),
]
