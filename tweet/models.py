from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from backend.utils import send_fcm_notification
from Auth.models import Profile


User = get_user_model()

channel = get_channel_layer()
# Create your models here.
class tweet(models.Model):
    body = models.CharField(max_length= 500)
    user = models.ForeignKey(User, related_name="tweets", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True)
    views = models.IntegerField(default=0)
    replied_to = models.CharField(max_length=20, default="")
    shares = models.IntegerField(default=0)
    retweeted_by = models.CharField(max_length=20,default="")

    class Meta:
        ordering = ["-created_at"]

class images(models.Model):
    image = models.ImageField(upload_to = "images")
    tweet = models.ForeignKey(tweet, on_delete=models.CASCADE, related_name="images")

class reply(models.Model):
    user = models.ForeignKey(User, related_name="replies", on_delete=models.CASCADE)
    reply = models.OneToOneField(tweet, on_delete=models.CASCADE)
    tweet = models.ForeignKey(tweet, related_name="replies", on_delete=models.CASCADE)
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_tweets")
    tweet = models.ForeignKey(tweet, on_delete=models.CASCADE, related_name = "likes")

class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="retweeted_tweets")
    retweeted_tweet = models.ForeignKey(tweet, on_delete=models.CASCADE, null=True)
    tweet = models.ForeignKey(tweet, on_delete=models.CASCADE, related_name = "retweets")
    

class hashtag(models.Model):
    hashtag = models.TextField()
    tweets = models.ManyToManyField(tweet)

    def __str__(self):
        return self.hashtag


@receiver(post_save, sender=tweet)
def post_save_tweet(sender,instance,created,  **kwargs):
    if created:
        words = instance.body.split(" ")
        for word in words:
            if word[0] == "#":
                hashobj, iscreated = hashtag.objects.get_or_create(hashtag = word[1:])
                hashobj.tweets.add(instance)
                hashobj.save()
        


        async_to_sync(channel.group_send)(
            "tweet_updates",
            {"type" : "new_tweet",
            "data": "new tweet",}
        )

        tokens = Profile.objects.all().values_list("fcm_token", flat=True)
        print(tokens)
        for token in tokens:
            if token:
                send_fcm_notification(token=token, title="New Tweet", body=f"{instance.user.username} shared a new tweet")
    
    

    
