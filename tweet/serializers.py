from rest_framework import serializers
from django.contrib.auth.models import User
from .models import tweet, images, Like, Retweet, hashtag

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = images
        fields = ['id', 'image']

class TweetSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required = False
    )
    user = serializers.StringRelatedField()
    images_data = ImageSerializer(source='images', many=True, read_only=True)
    name = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()
    isliked = serializers.SerializerMethodField()
    isretweeted = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    user_picture = serializers.SerializerMethodField()

    class Meta:
        model = tweet
        fields = ['id', 'body', 'user' ,'name','created_at', 'images', 'images_data',"likes","retweets","views","shares","isliked", "isretweeted", "retweeted_by", "replied_to" , "replies", "user_picture"]
        read_only = ["likes","retweets","views","shares"]
        ordering = ['-created_at']

    def create(self, validated_data):
        images_list = validated_data.pop('images', [])
        tweet_instance = tweet.objects.create(**validated_data)
        if not images_list:
            return tweet_instance
        for image in images_list:
            images.objects.create(tweet=tweet_instance, image=image)
        return tweet_instance

    def get_name(self, obj, *args, **kwargs):
        return obj.user.profile.Fame + " "+ obj.user.profile.Lname
    
    def get_likes(self, obj, *args, **kwargs):
        return obj.likes.count()
    
    def get_isliked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, tweet=obj).exists()
        return False
    
    def get_retweets(self, obj):
        return obj.retweets.count()
        
    def get_replies(self, obj):
        return obj.replies.count()
    
    def get_isretweeted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Retweet.objects.filter(user=request.user, tweet=obj).exists()
        return False
    def get_user_picture(self, obj):
        return obj.user.profile.picture.url

class HashtagSerializer(serializers.ModelSerializer):
    tweet_count = serializers.SerializerMethodField()
    class Meta:
        model = hashtag
        fields = ["hashtag", "tweet_count"]
    
    def get_tweet_count(self, obj, *args, **kwargs):
        return obj.tweets.count()