from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import *
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProfileSerializer


class RetrieveUpdateCreateProfileAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request, pk = None, *args, **kwargs):
        if not pk and request.user.is_authenticated:
            user = request.user
        else:
            user = get_object_or_404(User, id = pk)
        profile = get_object_or_404(Profile, user = user)
        sz = ProfileSerializer(profile)
        return Response(sz.data)

    def post(self, request, *args, **kwargs):
        sz = ProfileSerializer(data = request.data)
        if sz.is_valid():
            sz.save()
            return Response(sz.data, status=status.HTTP_200_OK)
        return Response(sz.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        if not request.user or not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        profile = get_object_or_404(Profile, user=request.user)
        sz = ProfileSerializer(profile, data=request.data)

        if sz.is_valid():
            sz.save()
            return Response(sz.data, status=status.HTTP_200_OK)

        return Response(sz.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class SearchUser(APIView):
    def get(self, request, query, *args, **kwargs):
        profile = Profile.objects.filter(user__username__icontains = query) 
        sz = ProfileSerializer(profile, many = True)
        return Response(sz.data)



class FollowUserAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username, *args, **kwargs):
        # Get the target user
        target_user = get_object_or_404(User, username=username)

        # Check if the logged-in user is following the target user
        qs = request.user.followings
        if qs.first().following.filter(username = target_user.username).exists():
        # Return appropriate respons
            return Response({"status": "Following"}, status=200)
        else:
            return Response({"status": "Follow"}, status=200)

    def post(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)

        if user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=400)

        # Get or create the follow object for the requesting user
        follow_obj, created = follow.objects.get_or_create()

        # Check if the user is already being followed
        if follow_obj.following.filter(id=user.id).exists():
            # Unfollow
            follow_obj.following.remove(user)
            return Response({"operation": f"Unfollowed {username}"})
        else:
            # Follow
            follow_obj.following.add(user)
            follow_obj.follower.add(request.user)
            return Response({"message": f"Followed {username}"})



class RegisterFCMToken(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        token = request.data.get('fcmToken')
        if token:
            profile  = get_object_or_404(Profile, user = request.user)
            profile.fcm_token = token
            profile.save()
            return Response(f"success changed the token for {request.user.username}", status=status.HTTP_200_OK)
        return Response("Token could not be created", status=status.HTTP_400_BAD_REQUEST)