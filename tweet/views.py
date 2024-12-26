from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import tweet, images, Like, Retweet, reply, hashtag
from .serializers import TweetSerializer, ImageSerializer, HashtagSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import clone_tweet_with_changes
from rest_framework import generics

# View for listing and creating tweets
class TweetCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a single tweet
class TweetDetailView(RetrieveUpdateDestroyAPIView):
    queryset = tweet.objects.all()
    serializer_class = TweetSerializer


class TweetListAPIView(ListAPIView):
    queryset = tweet.objects.all()
    serializer_class = TweetSerializer

class TweetReplies(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, pk):
        # Get all replies for the tweet with the given `pk`
        replies = reply.objects.filter(tweet__id=pk)
        replies_qs = [reply.reply for reply in replies]
        
        # Serialize the queryset
        sz = TweetSerializer(replies_qs, many=True)
        return Response(sz.data)
    
    def post(self, request, pk):
        if not request.user or not request.user.is_authenticated:
            return Response({"message" : "Authentication credentials were not provided"})
        tweetobj = tweet.objects.filter(id = pk).first()
        replytweetsz = TweetSerializer(data = request.data)
        if replytweetsz.is_valid():
            replytweet = replytweetsz.save(user = request.user)
            replytweet.replied_to = request.user.username
            replytweet.save()
        else:
            return Response({"message" : "Error occured!!"})
        replyobj = reply.objects.create(tweet = tweetobj, reply = replytweet, user = request.user)
        return Response({"Message" : "replied succesfully"})

class TweetRetweet(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        tweetobj = tweet.objects.get(id = pk)
        user = request.user
        retweetobj = Retweet.objects.filter(user = request.user, tweet = tweetobj).first()
        if Retweet.objects.filter(user = request.user, tweet = tweetobj).exists():
            retweetobj.delete()
            return Response({"message" : "retweet deleted"})
        newtweet = clone_tweet_with_changes(tweet_obj=tweetobj, field_name="retweeted_by", new_value=user.username)
        retweetobj = Retweet.objects.create(user=user, tweet = tweetobj, retweeted_tweet = newtweet)
        return Response({"message" : "retweet created"})
        

class TweetLikeAPI(APIView):
    permission_classess = [IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        tweetobj = tweet.objects.get(id = pk)
        user = request.user
        likeobj, created = Like.objects.get_or_create(tweet = tweetobj, user = user)
        if created:
            return Response({"operation" : "liked"})
        else:
            likeobj.delete()
        return Response({"operation" : "unliked"})

# View for listing and creatasdasding images for a specific tweet
class ImageListCreateView(APIView):
    def get(self, request, tweet_id):
        try:
            tweet_instance = tweet.objects.get(id=tweet_id)
        except tweet.DoesNotExist:
            return Response({"error": "Tweet not found."}, status=status.HTTP_404_NOT_FOUND)

        images_queryset = images.objects.filter(tweet=tweet_instance)
        serializer = ImageSerializer(images_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, tweet_id):
        try:
            tweet_instance = tweet.objects.get(id=tweet_id)
        except tweet.DoesNotExist:
            return Response({"error": "Tweet not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tweet=tweet_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TweetsUserList(APIView):
    def get(self, request, pk ,*args, **kwargs):
        qs = tweet.objects.filter(user__id = pk)
        sz = TweetSerializer(qs, many = True)
        return Response(sz.data)


class ListSearchHashtagAPI(APIView):
    def get(self, request, hq, *args, **kwargs):
        hashtagobjs = get_object_or_404(hashtag, hashtag = hq)
        sz = TweetSerializer(hashtagobjs.tweets, many = True)
        return Response(sz.data)
    
class ListHashtagAPI(generics.ListAPIView):
    queryset = hashtag.objects.all()
    serializer_class = HashtagSerializer
    