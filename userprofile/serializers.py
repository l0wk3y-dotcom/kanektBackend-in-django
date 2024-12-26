from rest_framework import serializers
from Auth.models import Profile, User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = "__all__"