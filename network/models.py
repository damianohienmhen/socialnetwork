from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    nickname = models.CharField(max_length=64, default="")
    followers= models.ManyToManyField('self', related_name="followers")
    
   
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.username,
        }
 
    
class Post(models.Model):
    post_content = models.CharField(max_length=75)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', default="")
    likes = models.ManyToManyField(User, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "post_content": self.post_content,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "user": self.user.username,
            "id": self.id,
            "likes":self.likes.count()
        }
    
    def __str__(self):
        return f"{self.user} ({self.post_content})"
        
   
    
        

    
