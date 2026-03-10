from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Create your models here.
class resources_post(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    file = CloudinaryField(resource_type ='raw',folder='pdfs')
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)


    def __str__(self):
        return self.title

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics/', default='profile_pics/sparks_profile.png')

    def __str__(self):
        return self.user.username

    