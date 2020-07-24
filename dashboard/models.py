from django.db import models
from datetime import datetime
from login.models import User
# Create your models here.

class Messages(models.Model):
    message = models.TextField()
    poster = models.ForeignKey(User, related_name="posted_messages", on_delete = models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comments(models.Model):
    comment = models.TextField()
    poster = models.ForeignKey(User, related_name="poster_comments", on_delete = models.CASCADE,null=True)
    message = models.ForeignKey(Messages, related_name='message_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)