from django.urls import path
from . import views
urlpatterns = [
    path("", views.TweetCreateView.as_view()),
    path("hashtag/<str:hq>", views.ListSearchHashtagAPI.as_view()),
    path("hashtag/", views.ListHashtagAPI.as_view()),
    path("list/", views.TweetListAPIView.as_view()),
    path("<int:pk>/like", views.TweetLikeAPI.as_view()),
    path("<int:pk>/retweet", views.TweetRetweet.as_view()),
    path("<int:pk>/replies", views.TweetReplies.as_view()),
    path("user/<int:pk>", views.TweetsUserList.as_view()),
]
