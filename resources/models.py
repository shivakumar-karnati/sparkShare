from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class resources_post(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField()
    file = models.FileField(upload_to='uploads/')
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.title

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics/', default='profile_pics/sparks_profile.png')

    def __str__(self):
        return self.user.username



















class blogPermissionPost(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    