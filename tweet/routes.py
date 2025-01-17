from django.urls import re_path
from . import consumers
ws_patterns = [
    re_path(r"ws/connect/$",consumers.TweetUpdateConsumer.as_asgi() )
]