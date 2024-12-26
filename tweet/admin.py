from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(tweet)
admin.site.register(hashtag)
admin.site.register(images)
admin.site.register(Like)
admin.site.register(Retweet)