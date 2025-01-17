import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
class TweetUpdateConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.group_name = "tweet_updates"
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send(json.dumps({"message" : "hello world"}))
    
    
    def new_tweet(self, event):
        self.send(json.dumps({"action" : "new_tweet"}))
        