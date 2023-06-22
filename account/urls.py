from django.urls import path
from account.views import (
    RegisterView,
    VerifyEmail,
    LoginView,
    LogoutView,
    ProfileApiView
    )
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email', VerifyEmail.as_view(), name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('<user_id>/profile/', ProfileApiView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]