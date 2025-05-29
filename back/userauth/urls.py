from django.urls import path
from .views import LogInApiView, RegisterView, PasswordChangeApiView, PasswordResetRequestView, \
    PasswordResetConfirmView, UserInfoChangeView

urlpatterns = [
    path('login/', LogInApiView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('info_change/', UserInfoChangeView.as_view(), name='user_info_change'),
    path('password-change/', PasswordChangeApiView.as_view(), name='password_change'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
