from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    password = serializers.CharField(required = False)
    username_create = serializers.CharField(required = False)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ["id","Fame","Lname","picture","bio","user","banner", "password", "username_create", "username", "followers", "following"]
    
    def get_username(self, obj, *args, **kwargs):
        return obj.user.username
    
    def update(self, instance, validated_data):
        # Update related `User` model
        username = validated_data.pop("username", None)  # Default to None if not provided
        if username:
            instance.user.username = username
            instance.user.save()

        # Update `Profile` model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def create(self, validated_data):
        print(validated_data)
        username = validated_data.pop("username_create", None)
        user = validated_data.pop("user", None)
        password = validated_data.pop("password", None)

        if not username:
            raise serializers.ValidationError("Username not provided")
        if not password:
            raise serializers.ValidationError("password not provided")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": f"This {username} is already taken."})
        
        userobj = User.objects.create(username= username)
        userobj.set_password(password)
        userobj.save()
        
        profile = Profile.objects.create(user = userobj, **validated_data)
        return profile
    
    def get_followers(self, obj, *args, **kwargs):
        return obj.user.followers.count()
    
    def get_following(self, obj, *args, **kwargs):
        return obj.user.followings.count()
    

       