from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    Fame = models.CharField(max_length=20)
    Lname = models.CharField(max_length=20)
    picture = models.ImageField(upload_to= "pp", default= "pp/default.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length = 200)
    banner = models.ImageField(upload_to="banners", default="banners/default.jpeg",)
    fcm_token = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.username + " | profile"

class follow(models.Model):
    follower = models.ManyToManyField(User, related_name="followings")
    following = models.ManyToManyField(User, related_name="followers")