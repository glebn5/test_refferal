from django.urls import path
from .views import SendCodeView, VerifyCodeView, user_profile, activate_invite_code
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('send-code/', SendCodeView.as_view(), name='send-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('profile/', user_profile, name='profile'),
    path('profile/activate/', activate_invite_code, name='activate-invite-code'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

