from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
# Create your models here.

User=get_user_model()

class profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    userid =models.IntegerField()
    bio = models.TextField(blank=True)
    profileImg = models.ImageField(upload_to="profile_img",default='bloglist-3.jpg')
    location = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user =models.CharField(max_length=100)
    image =models.ImageField(upload_to='post_image')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)

    
    def __str__(self):
        return self.user
    
class likepost(models.Model):
    username = models.CharField(max_length=100)
    post_id = models.CharField(max_length=500)

    def __str__(self):
        return self.username
    

class followscount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self) :
        return self.user
