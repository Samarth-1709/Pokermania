from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register

urlpatterns = [
    path('upload_bot/', views.upload_bot, name='upload_bot'),
    path('auth/register/', register, name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('',views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('my_bots/', views.my_bots, name='my_bots'),
    path('replay/<int:game_id>/', views.replay, name='replay'),
    path('deploy_bot/', views.deploy_bot, name='deploy_bot'),
]
