from django.urls import path
from .views import LogInApiView, RegisterView, PasswordChangeApiView, PasswordResetRequestView, \
    PasswordResetConfirmView

urlpatterns = [
    path('user/login/', LogInApiView.as_view(), name='login'),
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/password-change/', PasswordChangeApiView.as_view(), name='password_change'),
    path('user/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('user/password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
