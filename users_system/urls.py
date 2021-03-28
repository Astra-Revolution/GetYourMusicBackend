from django.urls import path

from .views import register, user_detail, forgot_password, reset_password, \
    profiles_list, create_profiles, profiles_detail, musicians_list, organizers_list, \
        musicians_genres, musicians_instruments
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_token'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('users/<int:user_id>/', user_detail, name='user_detail'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('reset-password/', reset_password, name='reset-password'),
    path('profiles/', profiles_list, name='profiles_list'),
    path('users/<int:user_id>/profiles/', create_profiles, name='create_profiles'),
    path('profiles/<int:profile_id>/', profiles_detail, name='profile_detail'),
    path('musicians/', musicians_list, name='musicians_list'),
    path('organizers/', organizers_list, name='organizers_list'),
    path('musicians/<int:musician_id>/genres/<genre_id>/', musicians_genres, name='musicians_genres'),
    path('musicians/<int:musician_id>/instruments/<instrument_id>/', musicians_instruments,
        name='musicians_instruments'),
]
