from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('login/',TokenObtainPairView.as_view(), name="jwt_login"),
    path('refresh/',TokenObtainPairView.as_view(), name="jwt_refresh"),
    path('profile/<int:pk>',views.RetrieveUpdateCreateProfileAPI.as_view(), name = "Get-profile"),
    path('profile/',views.RetrieveUpdateCreateProfileAPI.as_view(), name = "Get-profile"),
     path('search/<str:query>',views.SearchUser.as_view(), name = "Get-profile"),
     path('follow/<str:username>', views.FollowUserAPI.as_view())
]
